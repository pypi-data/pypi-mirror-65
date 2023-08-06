#!/usr/bin/env python3
"""
Transformer Generator with an additional memory module between the
encoder and decoder.
"""

from collections import OrderedDict
import numpy as np
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist

import parlai.agents.transformer.transformer as tsfrmr
from parlai.agents.transformer.modules import _create_embeddings, _build_encoder, \
    _normalize, TransformerDecoder, TransformerEncoderLayer
from parlai.core.build_data import modelzoo_path
from parlai.utils.distributed import is_distributed, num_workers
from parlai.core.logs import TensorboardLogger
import parlai.core.torch_generator_agent as tga
from parlai.utils.torch import neginf
from parlai.utils.misc import warn_once, round_sigfigs

try:
    from apex.normalization.fused_layer_norm import FusedLayerNorm as LayerNorm
except ImportError:
    warn_once("Installing APEX can give a significant speed boost.")
    from torch.nn import LayerNorm
LAYER_NORM_EPS = 1e-5  # Epsilon for layer norm.


def gumbel_softmax_topk(logits, k, tau=1, dim=-1):
    """
    This is like F.gumbel_softmax but with hard=True, and the top k indices
    set as 1's instead of just the top-1 set as 1. It's a one line difference,
    selecting indices with .topk() instead of one index with .max().

    See:
      https://pytorch.org/docs/stable/nn.html#torch.nn.functional.gumbel_softmax
      https://pytorch.org/docs/0.4.1/_modules/torch/nn/functional.html#gumbel_softmax
    """
    # Following pytorch 0.4.1
    eps = 1e-10
    gumbels = logits.data.new()
    shape = logits.shape
    uniform = gumbels.resize_(shape).uniform_() if gumbels is not None else torch.rand(shape)
    gumbels = - torch.log(eps - torch.log(uniform + eps))

    # Following pytorch 1.1.0
    # Problem is that adding these gumbels results in nans in softmax ->
    # idx in indices that is out of range -> runtime error in scatter
    # gumbels = -torch.empty_like(logits).exponential_().log()  # ~Gumbel(0,1)

    # Add gumbel noise
    gumbels = (logits + gumbels) / tau  # ~Gumbel(logits,tau)
    gumbels = logits / tau
    y_soft = gumbels.softmax(dim)

    # Do hard topk (with gradients from soft)
    indices = y_soft.topk(k, dim=dim)[1]
    y_hard = torch.zeros_like(logits).scatter_(dim, indices, 1.0)
    ret = y_hard - y_soft.detach() + y_soft

    return ret, y_soft

class MemBasic(nn.Module):
    """
    Memory module to be used with encoded Transformer inputs.
    """
    def __init__(
            self,
            mem_size,
            mem_dim,
            use_product_keys=False,
            n_queries=1,
            n_queries_write='first',
            query_network='lin_nobn',
            query_dropout=0.0,
            mem_maskout=0.0,
            dist_method='cos',
            mem_select_topk=-1,
            mem_select_topk_type='top',
            mem_select_topk_tau=1.0,
            mem_return_topk=-1,
            return_query=False,
            scale_mutual_prox=False,
            mem_write_topk=False,
            mem_write_used_thresh=-1,
            mem_write_age_thresh=-1,
            mem_write_age_thresh_schedule=None,
            mem_write_vals=False,
            writer=None, writer_name=None
        ):
        super().__init__()
        self.mem_size = mem_size
        self.mem_dim = mem_dim
        self.use_product_keys = use_product_keys
        self.n_queries = n_queries
        self.n_queries_write = n_queries_write
        self.query_network = query_network
        self.mem_maskout = mem_maskout
        self.query_dropout = nn.Dropout(query_dropout)
        self.dist_method = dist_method
        self.mem_select_topk = mem_select_topk
        self.mem_select_topk_type = mem_select_topk_type
        self.mem_select_topk_tau = mem_select_topk_tau
        self.mem_return_topk = mem_return_topk
        self.return_query = return_query

        self.scale_mutual_prox = scale_mutual_prox

        self.mem_write_topk = mem_write_topk
        self.mem_write_used_thresh = mem_write_used_thresh
        self.mem_write_age_thresh = mem_write_age_thresh
        self.mem_write_age_thresh_schedule = mem_write_age_thresh_schedule
        self.mem_write_vals = mem_write_vals

        self.used = torch.zeros(mem_size).byte()       # slots that have been used
        self.last_used = torch.zeros(mem_size)  # number of steps since last usage
        self.n_forwards = 0

        # Used for tensorboard logging
        self.writer = writer
        self.writer_name = writer_name
        self.used_mem_ks = [1, 5, 10]
        self.topk_used_slots = [torch.zeros(mem_size).byte() for k in self.used_mem_ks]
        self.used_mem_thresholds = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
        self.thresh_used_slots = [torch.zeros(mem_size).byte() for _ in range(len(self.used_mem_thresholds))]

        if not return_query:
            if use_product_keys:
                self.key_size = int(mem_size ** 0.5)
                self.key_dim = int(mem_dim / 2)
                self.keys1 = nn.Parameter(torch.Tensor(self.key_size, self.key_dim))
                self.keys2 = nn.Parameter(torch.Tensor(self.key_size, self.key_dim))
                self.values = nn.Parameter(torch.Tensor(mem_size, mem_dim))
                nn.init.xavier_uniform_(self.keys1)
                nn.init.xavier_uniform_(self.keys2)
                nn.init.xavier_uniform_(self.values)
            else:
                self.keys = nn.Parameter(torch.Tensor(mem_size, mem_dim))
                self.values = nn.Parameter(torch.Tensor(mem_size, mem_dim))
                nn.init.xavier_uniform_(self.keys)
                nn.init.xavier_uniform_(self.values)

            if n_queries == 1:
                self.q_proj = self._build_query_network(mem_dim)
            else:
                dim1 = int(mem_dim / n_queries)
                self.q_proj = nn.ModuleList([self._build_query_network(dim1, mem_dim) for _ in range(n_queries)])

        # Stored in forward pass
        self.topk_indices = None

    def _build_query_network(self, dim1, dim2=None):
        """
        Build network to project context into query.
        """
        dim2 = dim1 if (dim2 is None) else dim2

        layers = []
        if self.query_network == 'lin_nobn':
            return nn.Linear(dim1, dim2)
        if self.query_network == 'lin_bn':
            layers.append(nn.Linear(dim1, dim2))
            layers.append(nn.BatchNorm1d(dim2))
        elif self.query_network == 'ffn':
            layers.append(nn.Linear(dim1, dim1))
            layers.append(nn.BatchNorm1d(dim1))
            layers.append(nn.ReLU())
            layers.append(nn.Linear(dim1, dim2))
            layers.append(nn.BatchNorm1d(dim2))

        qnet = nn.Sequential(*layers)
        return qnet


    def log_mem_usage(self, topk_indices):
        """
        Keep track of memory usage (e.g. number of unused slots). Write to tensorboard.
        The notion of "unused" is based on how many memory slots are below some threshold,
        or the slots that have never been in the topk matches.

        :note: There is redundancy in calculations between this function and the write_to_mem
        function; we may want to track memory usage when not writing to memory as well.

        :param softmaxed: logits after softmax: [batch, mem_size]
        :param topk_indices: [batch, n_queries, k] LongTensors of length n_queries
        """
        if self.writer is None:
            return

        if (is_distributed() and (dist.get_rank() != 0)):  # only log on main worker
            return

        if self.n_queries > 1:
            # mean percent overlap of memories with multihead-queries
            # Jaccard := |A union B| / (|A| + |B| - |A difference B|)
            if self.n_forwards % 10 == 0:
                jaccards = []
                for i in range(self.n_queries):
                    for j in range(i+1, self.n_queries):
                        q1_topk = set(topk_indices[:,i,:].contiguous().view(-1).tolist())
                        q2_topk = set(topk_indices[:,j,:].contiguous().view(-1).tolist())
                        numer = len(q1_topk.difference(q2_topk))
                        denom = len(q1_topk.union(q2_topk))
                        jaccards.append(numer / float(denom))
                mean_jac = np.mean(jaccards)
                self.writer.log_metrics(self.writer_name, self.n_forwards,
                    {'n-queries-mean-jaccard': mean_jac})


        for i, k in enumerate(self.used_mem_ks):
            # Always update which slots were used. Don't log on every forward pass though.
            self.topk_used_slots[i][topk_indices.unique()] = 1
            if self.n_forwards % 10 == 0:
                num_never_used = self.mem_size - self.topk_used_slots[i].sum().item()
                percent_never_used = num_never_used / float(self.mem_size) * 100
                self.writer.log_metrics(self.writer_name, self.n_forwards,
                    {'percent-never-used-topk-{}'.format(k): percent_never_used})

    def log_mem_write(self, n_possible_writes, write_indices):
        """Tensorboard log stats related to memory writing."""
        if self.writer is None:
            return
        if (is_distributed() and (dist.get_rank() != 0)):  # only log on main worker
            return

        if self.n_forwards % 10 == 0:
            n_writes = write_indices.unique().size(0)  # in distr, diff workers may draw same indices
            perc_writes = n_writes / float(n_possible_writes) * 100
            self.writer.log_metrics(self.writer_name, self.n_forwards,
                {'batch-perc-writes': perc_writes})

            n_above_age = (self.last_used > self.mem_write_age_thresh).nonzero().size(0)
            perc_above_age = n_above_age / float(self.mem_size) * 100
            self.writer.log_metrics(self.writer_name, self.n_forwards,
                {'perc-mem-above-age': perc_above_age})

    def mutual_prox(self, dist):
        """
        Rescale the inner product distances to reduce hubness of points by
        upweighting points that are *mutually* close to each other. A rough
        version of the mutual proximity metric found in
        "Local and Global Scaling Reduce Hubs in Space" (Schnitzer, 2012)
        https://pdfs.semanticscholar.org/ffde/6c7a5d9e6c5db61d1ea3c3044b182a554534.pdf.

        Note: See commit history for how to compute the full (approximate) mutual
        proximity metric. However, because it involves a binary < comparison,
        there is no gradient. These scaling methods typically work as a post-processing
        step. In order to capture roughly the same idea, instead of calculating
        P(X < d) using the CDF, we compare each distance relative to the mean.
        Points are mutually proximal if they are relatively close, with respect to
        all other query / memory points.

        :param dist: tensor of cosine similarities / inner products (i.e. between queries
            and memory slots): [batch, msz]
        """
        bsz, msz = dist.size()

        # Scale distances to [0, ) so that closest points have a distance of 0.
        # Each query (row in dist_x) has a distribution P(X) of distances to memories
        # Each memory (column) has a distribution P(Y) of distances to queries
        dist_x = -dist + dist.max(dim=1)[0].unsqueeze(1)  # P(X): dist from query to memory; [bsz, msz]
        dist_y = -dist + dist.max(dim=0)[0]  # P(Y): dist from memory to query; [bsz, msz]

        # Queries / memories that have high means are hubs and should be downweighted
        x_mean = dist_x.mean(dim=1)  # mean dist from each query to memories; [bsz]
        y_mean = dist_y.mean(dim=0)  # mean dist from each memory to queries; [msz]

        # dividng by larger means -> downweights
        p_x = dist_x / x_mean.unsqueeze(1)
        p_y = dist_y / y_mean
        mutual_prox = p_x * p_y

        return mutual_prox

    def _update_used_mems_vars(self, topk_indices):
        """
        Track which slots were used in this batch. This updates two variables:
            self.used -- binary bit for whether a memory has ever been used before
            self.last_used -- counter for when each memory was last used.

        :param topk_indices: [bsz * n_q, k] LongTensor
        """
        used = torch.zeros(self.mem_size)
        used_indices = topk_indices.unique()
        used[used_indices] = 1  # used := used in this batch
        self.used[used_indices] = 1

        # Set used slots to 0, increment unused slots
        used = used.byte()
        self.last_used = torch.where(used, torch.zeros(self.mem_size), self.last_used + 1)

    def _update_mem_write_age_thresh(self):
        """Potentially increase age threshold if this hyperparameter has a schedule."""
        if self.mem_write_age_thresh_schedule is not None:
            for step, thresh in self.mem_write_age_thresh_schedule:
                if self.n_forwards > step:
                    self.mem_write_age_thresh = thresh

    def write_to_mem_get_indices(self, bsz):
        """
        Calculate which memory slots to write to.
        When in distributed mode, the rank-0 worker gets the N oldest available / first N unused
        memory slots, the rank-1 worker gets the next N oldest available / second N unused
        slots, etc.

        :return [m] LongTensor
            m may be in range [0, bsz]
        """
        # Prioritize writing to slots that have never been used.
        unused_indices = (self.used == 0).nonzero().squeeze(1)  # [n]
        n_unused_indices = unused_indices.size(0)

        if n_unused_indices >= bsz:
            if not is_distributed():
                write_indices = unused_indices[:bsz]
            else:
                rank = dist.get_rank()
                start_idx = rank * bsz
                end_idx = start_idx + bsz
                write_indices = unused_indices[start_idx:end_idx]
        else:
            # Get least recently used
            # available_indices := indices above age threshold
            # oldest_available_indices := oldest indices, relative to "available_indices"
            available_indices = (self.last_used > self.mem_write_age_thresh).nonzero().squeeze(1)  # [n_lru]

            if not is_distributed():
                top_n = min(bsz, available_indices.size(0))
                _, oldest_available_indices = self.last_used[available_indices].topk(top_n)
                lru_indices = available_indices[oldest_available_indices]
            else:
                # get up to bsz * n_workers oldest available indices and then slice out the portion
                # corresponding to this worker
                n_workers = num_workers()
                top_n = min(bsz * n_workers, available_indices.size(0))
                _, oldest_available_indices = self.last_used[available_indices].topk(top_n)
                lru_indices = available_indices[oldest_available_indices]

                # get this worker's indices
                rank = dist.get_rank()
                start_idx = rank * bsz
                end_idx = start_idx + bsz
                lru_indices = lru_indices[start_idx:end_idx]

            # combine (potentially) unused and LRU indices, prioritizing unused
            n_lru = lru_indices.size(0)
            if (n_lru > 0) and (n_unused_indices > 0):  # concatenate the unused slots with the lru slots
                n_lru_write = bsz - n_unused_indices
                lru_write_indices = lru_indices[torch.randperm(n_lru)[:n_lru_write]]
                write_indices = torch.cat([unused_indices, lru_write_indices], dim=0).unique()
            elif (n_lru > 0) and (n_unused_indices == 0):
                write_indices = lru_indices
            elif (n_lru == 0) and (n_unused_indices > 0):
                write_indices = unused_indices
            else:
                write_indices = torch.LongTensor()

        return write_indices

    def _write_to_mem(self, write_indices, q_proj, vals=None):
        """
        Write to keys and values.

        :param write_indices: [n] LongTensor
        :param q_proj: [m, dim]
        :param vals: [m, dim]

        In distributed mode, n can be up to bsz * num_workers.
        """
        n = write_indices.size(0)
        if n > 0:
            # casting occurs when fp16=true -- parameter will be (Cuda)HalfTensor instead of Float
            q_proj = q_proj.type(self.keys.type()) if (self.keys.type() != q_proj.type()) else q_proj
            self.keys.data[write_indices] = q_proj[:n]
            if vals is not None:
                vals = vals.type(self.values.type()) if (self.values.type() != vals.type()) else vals
                self.values.data[write_indices] = vals[:n]

    def write_to_mem(self,
                     q_proj,
                     vals=None):
        """
        Write queries to memory based on which memories have been used before
        and used recently. Assumes _update_used_mems_vars() has been called. as this
        calls write_to_mem_get_indices(), which uses those vars (self.used, self.last_used).

        :param q_proj: [batch, dim]
        :param vals: [batch, dim] used when self.mem_write_vals=True
        """
        if not is_distributed():
            bsz = q_proj.size(0)
            write_indices = self.write_to_mem_get_indices(bsz)
            self._write_to_mem(write_indices, q_proj, vals)
            self.log_mem_write(bsz, write_indices)
            return

        bsz = q_proj.size(0)
        n_workers = num_workers()
        rank = dist.get_rank()

        # Sync self.used and self.last_used, which ewre updated by _update_used_mems_vars(),
        # before getting which indices to write to.
        # self.write_to_mem_get_indices() uses self.used and self.last_used
        all_used = torch.ByteTensor(n_workers, self.mem_size).zero_()
        all_last_used = torch.FloatTensor(n_workers, self.mem_size).zero_()
        all_used[rank, :] = self.used
        all_last_used[rank, :] = self.last_used
        all_used = all_used.cuda()
        all_last_used = all_last_used.cuda()
        dist.all_reduce(all_used)
        dist.all_reduce(all_last_used)
        self.used = all_used.max(dim=0)[0].cpu()
        self.last_used = all_last_used.min(dim=0)[0].cpu()

        # Get memory slots to write and sync across workers
        write_indices = self.write_to_mem_get_indices(bsz)
        if next(self.parameters()).is_cuda:
            write_indices = write_indices.cuda()
        n_writes = write_indices.size(0)

        # start and end indices for *writing*
        start_write = bsz * rank
        end_write = start_write + n_writes
        end_worker = bsz * (rank + 1)

        all_write_indices = torch.LongTensor(bsz * n_workers)\
            .to(write_indices.get_device()).zero_()
        all_write_indices[start_write:end_worker] = -1  # -1 (no write) for this worker
        all_write_indices[start_write:end_write] = write_indices
        dist.all_reduce(all_write_indices)

        # Write keys and values
        write_keys = q_proj[:n_writes]
        all_write_keys = torch.FloatTensor(bsz * n_workers, self.mem_dim)\
            .to(write_keys.get_device()).zero_()
        all_write_keys[start_write:end_write] = write_keys
        dist.all_reduce(all_write_keys)

        all_write_vals = None
        if vals is not None:
            write_vals = vals[:n_writes]
            all_write_vals = torch.FloatTensor(bsz * n_workers, self.mem_dim)\
                .to(write_vals.get_device()).zero_()
            all_write_vals[start_write:end_write] = write_vals
            dist.all_reduce(all_write_vals)

        # all_write_indices was filled with -1 upon init to identify unused
        # rows (every batch can write up to bsz slots, but this may
        # be less depending on LRU).
        mask = all_write_indices >= 0
        all_write_indices = all_write_indices[mask]
        all_write_keys = all_write_keys[mask]
        all_write_vals = all_write_vals[mask]

        self._write_to_mem(all_write_indices, all_write_keys, all_write_vals)
        self.log_mem_write(bsz * n_workers, all_write_indices)

    def cosine_sim(self, x1, x2=None, eps=1e-8):
        """
        Returns the pairwise cosine similarities, similar to scipy's
        cdist. (There is a cdist in pytorch now, but not for cosine
        similarity).

        :param x1: [m, dim]
        :param x2: [n, dim]
            If None, uses x1 as x2.

        :returns: [m,n] tensor where [i,j] is the cosine similarity between
            x1[i] and x2[j].
        """
        x2 = x1 if x2 is None else x2
        w1 = x1.norm(p=2, dim=1, keepdim=True)
        w2 = w1 if x2 is x1 else x2.norm(p=2, dim=1, keepdim=True)
        cos_sim = torch.mm(x1, x2.t()) / (w1 * w2.t()).clamp(min=eps)
        return cos_sim

    def cartesian_product(self, a, b):
        """
        Compute the batched cartesian product between two matrices
        (e.g. two top-k subquery-prodkey similarities, each of size [bsz, k])

        :param a: [n, m1] Tensor
        :param b: [n, m2] Tensor

        :returns prod: [n, m1 * m2, 2] Tensor
            prod[a][i][j] := for a-th item in batch, (i,j)-th cartesian product

        """
        n, m1 = a.shape
        n, m2 = b.shape

        a_rep = a.unsqueeze(-1).repeat(1, 1, m2).unsqueeze(-1)  # [n, m1, m2, 1]
        b_rep = b.repeat(1, m1).view(n, m1, m2).unsqueeze(-1)  # [n, m1, m2, 1]
        prod = torch.cat([a_rep, b_rep], dim=3)  # [n, m1, m2, 2]
        prod = prod.view(n, m1 * m2, 2)  # [n, m1 * m2, 2]
        return prod

    def forward(self, query, vals=None, use_mem_idx=None):
        """
        :param query: [batch, dim]
            I.e. encoded context.
        :param vals: [batch, dim]
            Encoded targets to be written to memory values.
        :param use_mem_idx: int
            Used during inference to analyze memory. Returns value found in use_mem_idx.

        :return: [batch, dim]
            or [batch, self.mem_return_topk, dim] if self.mem_return_topk >= 1
        """
        if self.return_query:
            return query

        bsz, dim = query.size()

        if use_mem_idx is not None:
            mem_value = self.values[use_mem_idx,:]
            result = torch.stack([mem_value for _ in range(bsz)], dim=0)
            return result

        # Pass context through query network to get query for memory
        q_projs = None                      # list of length n_queries of [bsz, dim]
        if self.n_queries == 1:
            q_proj = self.q_proj(query)     # [bsz, dim]
            q_proj = self.query_dropout(q_proj)
            q_projs = [q_proj]
        else:
            queries = query.view(bsz, self.n_queries, int(dim / self.n_queries))       # [bsz, n_q, dim / n_q]
            q_projs = [self.q_proj[i](queries[:,i,:]) for i in range(self.n_queries)]  # list of [bsz, dim]
            q_projs = [self.query_dropout(q_proj) for q_proj in q_projs]

        # Calculate memory result using query(s)
        q_proj = torch.cat(q_projs, dim=0)   # [bsz * n_q, dim]
        mem_result, topk_scores, topk_indices, vals_softmax = self.calc_mem_result(q_proj)
        # [bsz * n_q, dim]; [bsz * n_q, k]; [bsz * n_q, k] ; [bsz * n_q, vocab]

        # Reshape mem result (combine in the case of multiple queries)
        if self.mem_return_topk >= 1:
            mem_result = mem_result.view(bsz, self.n_queries, self.mem_return_topk, dim)   # [bsz, n_q, retk, dim]
            mem_result = mem_result.mean(dim=1)                         # [bsz, retk, dim]
        else:
            mem_result = mem_result.view(bsz, self.n_queries, dim)      # [bsz, n_q, dim]
            mem_result = mem_result.mean(dim=1)                         # [bsz, dim]

        # Logging, updating variables, etc
        # if multiple queries, log_mem_usage() just tracks first vals_softmax
        self.log_mem_usage(topk_indices.view(bsz, self.n_queries, -1))
        self._update_used_mems_vars(topk_indices)      # must be called before write_to_mem()
        self.topk_indices = topk_indices
        self.n_forwards += 1
        self._update_mem_write_age_thresh()

        # Write to memory
        if self.training and self.mem_write_topk:
            # when there are multiple queries, we have to decide which query to write to the keys
            if self.n_queries_write == 'first':
                idx = 0
            elif self.n_queries_write == 'random':
                idx = random.choice(range(self.n_queries))
            self.write_to_mem(q_projs[idx], vals=vals)

        return mem_result

    def calc_mem_result(self, q_proj):
        """
        Given the query, calculate (topk) memories and compute weighted sum of values.

        :param q_proj: [batch * n_queries, dim]

        :return:
            result: [batch * n_queries, dim]
            topk_scores: [batch * n_queries, k]
                - "raw" scores (before softmax) of top similarities
            topk_indices: [batch * n_queries, k]
            vals_softmax: [batch * n_queries, mem_size]
                - post softmax values of similarities between query and memories
        """
        result, topk_scores, topk_indices, vals_softmax = None, None, None, None

        #
        # Product keys
        #
        if self.use_product_keys:
            # split query into two sub queries
            bsz = q_proj.size(0)
            key_len = int(q_proj.size(1) / 2)
            q_proj1 = q_proj[:, :key_len]
            q_proj2 = q_proj[:, key_len:]

            # calculate softmaxed similarities b/n each sub-query and each product key set
            dist1 = self.cosine_sim(q_proj1, self.keys1)  # [bsz * n_q, key_size]
            dist2 = self.cosine_sim(q_proj2, self.keys2)  # [bsz * n_q, key_size]
            batch_k = self.mem_select_topk
            topk1, topk_indices1 = dist1.topk(batch_k, dim=1)  # [bsz * n_q, k]
            topk2, topk_indices2 = dist2.topk(batch_k, dim=1)  # [bsz * n_q, k]
            topk_softmax1 = F.softmax(topk1.float(), dim=1).type_as(dist1)  # [bsz * n_q, k]
            topk_softmax2 = F.softmax(topk2.float(), dim=1).type_as(dist2)  # [bsz * n_q, k]

            # calculate cartesian product between each subquery-prodkey
            concat_scores = self.cartesian_product(topk_softmax1, topk_softmax2)  # [bsz * n_q, k^2, 2]
            concat_indices = self.cartesian_product(topk_indices1, topk_indices2) # [bsz * n_q, k^2, 2]
            all_scores = concat_scores.sum(2)  # [bsz * n_q, k^2]  # score is sum of two key scores
            all_indices = concat_indices[:, :, 0] * self.key_size + concat_indices[:, :, 1]  # [bsz * n_q, k^2]

            # all_indices are used to index into the values, ranges from [0, mem_size-1] ([0, key_size ** 2 - 1])
            # best_indices used to index into all_indices
            # calculate topk_indices for eval, logging, write mem
            topk_scores, best_indices = torch.topk(all_scores, k=batch_k, dim=1, largest=True, sorted=True)  # [bsz * n_q, k]
            topk_indices = all_indices.gather(1, best_indices)
            self.topk_indices = topk_indices
            vals_wgts = topk_scores
            vals_softmax = torch.zeros(bsz, self.mem_size).to(topk_indices.get_device())\
                .scatter_(1, topk_indices, F.softmax(topk_scores))

            # compute memory result as weighted values
            topk_values = F.embedding(topk_indices, self.values, sparse=False)  # [bsz * n_q, k, dim]
            vals_wgts = vals_wgts.unsqueeze(1)  # [bsz * n_q, 1, k]
            result = torch.bmm(vals_wgts, topk_values)  # [bsz * n_q, 1, dim]
            result = result.squeeze(1)  # [bsz * n_q, dim]

            return result, topk_scores, topk_indices, vals_softmax


        # Calculate similarities between query and keys
        if self.dist_method == 'cos':
            dist = self.cosine_sim(q_proj, self.keys)
        elif self.dist_method == 'dot':
            dist = torch.mm(q_proj, self.keys.t())  # [bsz * n_q, mem_size]

        if self.scale_mutual_prox:
            dist = self.mutual_prox(dist)

        if self.training and self.mem_maskout > 0:
              # n=1 on binomial -> bernoulli; " 1 - ..." so that maskout=0.2 corresponds to keeping 80%
            maskout = [1 - np.random.binomial(1, self.mem_maskout) for _ in range(self.mem_size)]
            maskout = torch.Tensor(maskout).to(dist.get_device())  # [mem_size]
            dist *= maskout

        # Calculate weights to use for blending memory values
        # vals_softmax and topk_indices are also calculated for logging, metrics, and writing to memory
        if self.mem_select_topk < 1:
            vals_wgts = F.softmax(dist.float(), dim=1).type_as(q_proj)
            vals_softmax = vals_wgts
            topk_scores, topk_indices = vals_wgts.topk(10, dim=1)[1]
        else:
            batch_k = self.mem_select_topk
            if isinstance(self.mem_select_topk, list):
                batch_k = random.choice(self.mem_select_topk)

            if self.mem_select_topk_type == 'top':
                # only take softmax over topk values
                # cast to float and back for stability in fp16 mode
                topk_scores, topk_indices = dist.topk(batch_k, dim=1)  # [bsz * n_q, k]
                topk_softmax = F.softmax(topk_scores.float(), dim=1).type_as(dist)
                vals_wgts = torch.zeros_like(dist).scatter_(1, topk_indices, topk_softmax)
                vals_softmax = vals_wgts
            elif self.mem_select_topk_type == 'gumbel':
                vals_wgts, vals_softmax = gumbel_softmax_topk(dist, batch_k, self.mem_select_topk_tau)
                topk_scores, topk_indices = vals_wgts.topk(batch_k, dim=1)

        # Use weights from above to blend together memory values
        if self.mem_return_topk >= 1:
            # import pdb; pdb.set_trace()
            result = topk_softmax.unsqueeze(-1) * self.values[topk_indices, :]
            # result = self.values[topk_indices,:]  # [bsz * n_q, k, dim]
        else:
            result = torch.mm(vals_wgts, self.values)  # [bsz * n_q, dim]

        return result, topk_scores, topk_indices, vals_softmax


class TransformerEncoderMemBasic(nn.Module):
    """
    Combines a Transformer encoder and a Memory module.
    """
    def __init__(
            self,
            tsfrmr_encoder,
            mem_size,
            mem_dim,
            use_product_keys=False,
            n_queries=1,
            n_queries_write='first',
            query_network='lin_nobn',
            query_dropout=0.0,
            mem_maskout=0.0,
            dist_method='cos',
            mem_select_topk=-1,
            mem_select_topk_type='top',
            mem_select_topk_tau=1.0,
            mem_return_topk=-1,
            mem_return_query=False,
            scale_mutual_prox=False,
            mem_write_topk=False,
            mem_write_used_thresh=-1,
            mem_write_age_thresh=-1,
            mem_write_age_thresh_schedule=None,
            mem_write_vals=False,
            mem_dropout=0.0,
            mem_result_scale_to=None,
            query_mem_locality_loss=False,
            enc_mem_combine='sum',
            enc_mem_alpha=0.5,
            enc_mem_alpha_rand=False,
            enc_mem_dropout=0.0,
            use_enc_mem_layernorm=False,
            use_extra_enc_layer=False,
            writer=None,
            writer_name=None
        ):
        super().__init__()

        if (mem_return_topk > 0) and (enc_mem_combine != 'append'):
            raise AssertionError(
                'If --mem-return-topk is used, --enc-mem-combine must equal "append".'
            )

        self.tsfrmr_encoder = tsfrmr_encoder
        self.mem_size = mem_size
        self.mem_dim = mem_dim  # use same as esz
        self.dist_method = dist_method

        self.mem_select_topk = mem_select_topk
        self.mem_select_topk_type = mem_select_topk_type
        self.mem_select_topk_tau = mem_select_topk_tau
        self.mem_return_topk = mem_return_topk
        self.mem_return_query = mem_return_query
        self.scale_mutual_prox = scale_mutual_prox
        self.mem_write_topk = mem_write_topk
        self.mem_write_used_thresh = mem_write_used_thresh
        self.mem_write_age_thresh = mem_write_age_thresh
        self.mem_write_vals = mem_write_vals

        self.mem_dropout = nn.Dropout(mem_dropout)
        self.mem_result_scale_to = mem_result_scale_to
        self.query_mem_locality_loss = query_mem_locality_loss

        self.enc_mem_combine = enc_mem_combine
        self.enc_mem_alpha = enc_mem_alpha
        self.enc_mem_alpha_rand = enc_mem_alpha_rand
        self.enc_mem_dropout = enc_mem_dropout
        self.use_enc_mem_layernorm = use_enc_mem_layernorm
        if use_enc_mem_layernorm:
            self.enc_mem_layernorm = LayerNorm(self.mem_dim, eps=LAYER_NORM_EPS)
        self.use_extra_enc_layer = use_extra_enc_layer
        if use_extra_enc_layer:
            self.extra_enc_layer = TransformerEncoderLayer(
                self.tsfrmr_encoder.n_heads,
                self.tsfrmr_encoder.embedding_size,
                self.tsfrmr_encoder.ffn_size,
                dropout=self.tsfrmr_encoder.dropout.p,
                activation=self.tsfrmr_encoder.layers[0].activation,
                variant=self.tsfrmr_encoder.variant
            )

        self.writer = writer
        self.writer_name = writer_name

        self.memory = MemBasic(
            mem_size, mem_dim,
            use_product_keys,
            n_queries,
            n_queries_write,
            query_network,
            query_dropout,
            mem_maskout,
            dist_method,
            mem_select_topk, mem_select_topk_type, mem_select_topk_tau,
            mem_return_topk,
            mem_return_query,
            scale_mutual_prox,
            mem_write_topk, mem_write_used_thresh,
            mem_write_age_thresh, mem_write_age_thresh_schedule,
            mem_write_vals,
            writer=writer, writer_name=writer_name)

        # Stored in forward pass (potentially)
        self.mem_query = None
        self.mem_result = None

    def forward(self, input, positions=None, segments=None, targets=None, use_mem_idx=None):
        """
        :param input: FloatTensor of shape [batch, seq_len]
        :param positions: ByteTensor of shape [batch, seq_len], filled with 1 when
            inside the sequence and 0 outside. If None, mask is created
        :param segments:
        :param targets FloatTensor of shape [batch, seq_len]
            used when self.mem_write_vals=True
        """
        batch_size, seq_len = input.size()

        # Short circuit when using a specific memory slot
        if (use_mem_idx is not None) and (self.enc_mem_alpha == 0):
            mem_result = self.memory(input.float(), use_mem_idx=use_mem_idx).type_as(input)
            output = torch.stack([mem_result for _ in range(seq_len)], dim=1)  # [bsz, len, dim]
            mask = torch.ones(batch_size, seq_len).to(output.get_device())
            if self.enc_mem_combine == 'append':
                mask[:,:seq_len-1] = 0
            return output, mask

        # Use the mean of encoded inputs as the query to the memory
        enc_input, mask = self.tsfrmr_encoder(input, positions, segments)  # [bsz, len, esz]; [bsz, len]
        divisor = mask.float().sum(dim=1).unsqueeze(-1).clamp(min=1).type_as(enc_input)  # [bsz, 1]
        mem_query = enc_input.sum(dim=1) / divisor  # [bsz, dim]

        mem_vals = None
        if self.mem_write_vals and (targets is not None):
            enc_tgts, tgts_mask = self.tsfrmr_encoder(targets, positions, segments)  # [bsz, len, esz]; [bsz, len]
            divisor = tgts_mask.float().sum(dim=1).unsqueeze(-1).clamp(min=1).type_as(enc_tgts)  # [bsz, 1]
            mem_vals = enc_tgts.sum(dim=1) / divisor  # [bsz, dim]

        mem_result = self.memory(mem_query.float(), vals=mem_vals, use_mem_idx=use_mem_idx).type_as(mem_query)
        self.mem_result = mem_result
        if self.mem_result_scale_to is not None:
            mem_result *= (self.mem_result_scale_to / mem_result.norm())

        if self.query_mem_locality_loss:
            self.mem_query = mem_query
            self.mem_result = mem_result

        # Currently, TransformerGenMemBasic uses a TransformerDecoder as the decoder
        # To attend over encoded inputs and memory result, either:
        # a) expand memory result along the sequence dimension and sum with encoded inputs
        # b) append memory result to encoded inputs
        if self.enc_mem_combine == 'sum':
            mem_result_rep = torch.stack([mem_result for _ in range(seq_len)], dim=1)  # [bsz, len, dim]
            mem_result_rep = self.mem_dropout(mem_result_rep)
            weights = [self.enc_mem_alpha, 1 - self.enc_mem_alpha]
            if self.training and self.enc_mem_alpha_rand:  # assign random weights (that sum to 1)
                enc_weight = random.uniform(0, 1)
                mem_weight = 1 - enc_weight
                weights = [enc_weight, mem_weight]
            if self.training and (self.enc_mem_dropout > 0.0):  # "dropout" either the encoded inputs or the memory result
                if random.uniform(0, 1) < self.enc_mem_dropout:
                    weights = random.choice([[1,0], [0,1]])
            output = weights[0] * enc_input + weights[1] * mem_result_rep

        elif self.enc_mem_combine == 'append':
            mem_result = self.mem_dropout(mem_result)
            append_len = self.mem_return_topk if (self.mem_return_topk > 0) else 1
            if self.mem_return_topk < 0:  # mem_result is [bsz, dim] (blended memories); o.w. [bsz, k, dim]
                mem_result = mem_result.unsqueeze(1)

            output = torch.cat([enc_input, mem_result], dim=1)  # [bsz, len+k, dim]

            # Alter and append to mask
            if self.enc_mem_alpha == 1.0:  # attend only to encoded inputs
                mask_append = torch.zeros(batch_size, append_len)
            elif self.enc_mem_alpha == 0.5:  # attend to both
                mask_append = torch.ones(batch_size, append_len)
            elif self.enc_mem_alpha == 0.0:  # attend only to memory result
                mask.fill_(0)
                mask_append = torch.ones(batch_size, append_len)
            mask_append = mask_append.type_as(mask).to(mask.get_device())
            mask = torch.cat([mask, mask_append], dim=1)  # [bsz, len+k]

        # Additional transformations and combinations of context and memory
        if self.use_enc_mem_layernorm:
            output = self.enc_mem_layernorm(output)
        if self.use_extra_enc_layer:
            output = self.extra_enc_layer(output, mask)

        return output, mask


def _build_trsfrmr_mem_decoder(
    opt, dictionary, embedding=None, padding_idx=None, n_positions=1024, n_segments=0
    ):
    return TransformerDecoderMemBasic(
        opt['n_heads'],
        opt['n_layers'],
        opt['embedding_size'],
        opt['ffn_size'],
        len(dictionary),
        embedding=embedding,
        dropout=opt['dropout'],
        attention_dropout=opt['attention_dropout'],
        relu_dropout=opt['relu_dropout'],
        padding_idx=padding_idx,
        learn_positional_embeddings=opt['learn_positional_embeddings'],
        embeddings_scale=opt['embeddings_scale'],
        n_positions=n_positions,
        activation=opt['activation'],
        variant=opt['variant'],
        n_segments=n_segments,

        # specific to MemBasic
        dec_zeroout=opt['dec_zeroout'],
        dec_maskout=opt['dec_maskout'],
    )

class TransformerDecoderMemBasic(TransformerDecoder):
    def __init__(
            self,
            n_heads,
            n_layers,
            embedding_size,
            ffn_size,
            vocabulary_size,
            embedding=None,
            dropout=0.0,
            attention_dropout=0.0,
            relu_dropout=0.0,
            embeddings_scale=True,
            learn_positional_embeddings=False,
            padding_idx=None,
            n_positions=1024,
            n_segments=0,
            variant='aiayn',
            activation='relu',

            dec_zeroout=0.0,
            dec_maskout=0.0
        ):
        super(TransformerDecoderMemBasic, self).__init__(
            n_heads,
            n_layers,
            embedding_size,
            ffn_size,
            vocabulary_size,
            embedding,
            dropout,
            attention_dropout,
            relu_dropout,
            embeddings_scale,
            learn_positional_embeddings,
            padding_idx,
            n_positions,
            n_segments,
            variant,
            activation
        )

        # Add on MemBasic specific methods
        self.dec_zeroout = dec_zeroout
        self.dec_maskout = dec_maskout
        if dec_zeroout > 0:
            self.forward = self.decoder_zeroout_forward
        if dec_maskout > 0:
            for layer in self.layers:
                # TODO: Prob want to have the same mask for all layers. Currently it's
                # stochastic (each TransformerDecoderLayer calls create_selfattn_mask)
                layer._create_selfattn_mask = self._decoder_create_selfattn_mask

    def decoder_zeroout_forward(self, input, encoder_state, incr_state=None):
        """
        Forward pass.
        :param LongTensor[batch,seqlen] input:
            The decoder inputs (partial or full decoded token IDs).
        :param encoder_state:
            Output from the encoder module forward pass.
        :param incr_state:
            Ignored. Should always be ``None`` in this version.
        """
        encoder_output, encoder_mask = encoder_state

        seq_len = input.size(1)
        positions = input.new(seq_len).long()
        positions = torch.arange(seq_len, out=positions).unsqueeze(0)
        tensor = self.embeddings(input)
        if self.embeddings_scale:
            tensor = tensor * np.sqrt(self.dim)
        if self.variant == 'xlm':
            tensor = _normalize(tensor, self.norm_embeddings)
        if positions.max().item() > self.n_positions:
            warn_once(
                'You are inputting a sequence of {x} length, but only have '
                '--n-positions {y}. Set --truncate or increase --n-positions'.format(
                    x=positions.max().item(), y=self.n_positions
                )
            )
        pos_embeddings = self.position_embeddings(positions).expand_as(tensor)
        tensor = tensor + pos_embeddings

        # Zeroout: only use position embeddings
        if self.training:
            if random.uniform(0,1) < self.dec_zeroout:
                tensor = pos_embeddings

        tensor = self.dropout(tensor)  # --dropout

        for layer in self.layers:
            tensor = layer(tensor, encoder_output, encoder_mask)

        return tensor, None

    def _decoder_create_selfattn_mask(self, x):
        # figure out how many timestamps we need
        bsz = x.size(0)
        time = x.size(1)
        # make sure that we don't look into the future
        mask = torch.tril(x.new(time, time).fill_(1))

        # Maskout: don't attend to previous timesteps
        if self.training:
            if random.uniform(0,1) < self.dec_maskout:
                mask = torch.eye(time)
                mask = mask.cuda() if x.is_cuda else mask

        # broadcast across batch
        mask = mask.unsqueeze(0).expand(bsz, -1, -1)
        return mask

class TransformerGenMemBasicModel(tga.TorchGeneratorModel):
    """
    Encoder-Decoder Transformer with a Memory module to help decoding.
    """
    def half(self):
        """Needed when fp16=true and writing to memory."""
        r = super().half()
        r.encoder.memory.float()
        return r

    def __init__(self, opt, dictionary):
        self.pad_idx = dictionary[dictionary.null_token]
        self.start_idx = dictionary[dictionary.start_token]
        self.end_idx = dictionary[dictionary.end_token]
        super().__init__(self.pad_idx, self.start_idx, self.end_idx)
        self.embeddings = _create_embeddings(
            dictionary, opt['embedding_size'], self.pad_idx
        )

        if opt.get('n_positions'):
            # if the number of positions is explicitly provided, use that
            n_positions = opt['n_positions']
        else:
            # else, use the worst case from truncate
            n_positions = max(
                opt.get('truncate') or 0,
                opt.get('text_truncate') or 0,
                opt.get('label_truncate') or 0
            )
            if n_positions == 0:
                # default to 1024
                n_positions = 1024
        n_segments = opt.get('n_segments', 0)

        if n_positions < 0:
            raise ValueError('n_positions must be positive')

        self.writer = None
        self.writer_name = None
        if (opt['tensorboard_log']) and (self.training):
            try:
                if (not is_distributed()) or \
                    (is_distributed() and (dist.get_rank() == 0)):
                    self.writer = TensorboardLogger(opt)
                    self.writer_name = opt['datatype']
            except Exception as e:
                pass

        self.tsfrmr_encoder = _build_encoder(
            opt, dictionary, self.embeddings, self.pad_idx, reduction_type=None,
            n_positions=n_positions, n_segments=n_segments,
            )

        # Checks
        assert opt['n_queries'] in [1, opt.get('n_heads', 1)]
        # some things aren't implemented for product keys
        # this list of assertions isn't necessarily exhaustive
        if opt['use_product_keys']:
            assert int(opt['mem_size'] ** 0.5) == (opt['mem_size'] ** 0.5)  # square of an int
            assert opt['mem_maskout'] == 0
            assert opt['scale_mutual_prox'] is False
            assert opt['mem_write_topk'] is False

        # Parse out list arguments
        mem_select_topk = int(opt['mem_select_topk']) if (',' not in str(opt['mem_select_topk'])) \
            else [int(k) for k in opt['mem_select_topk'].split(',')]
        age_schedule = None
        if opt['mem_write_age_thresh_schedule'] is not None:
            age_schedule = opt['mem_write_age_thresh_schedule'].split(',')
            age_schedule = [s.split(':') for s in age_schedule]
            age_schedule = [(int(s), int(a)) for s, a in age_schedule]

        self.encoder = TransformerEncoderMemBasic(
            self.tsfrmr_encoder,
            opt['mem_size'],
            opt['mem_dim'],
            use_product_keys=opt['use_product_keys'],
            n_queries=opt['n_queries'],
            n_queries_write=opt['n_queries_write'],
            query_network=opt['query_network'],
            query_dropout=opt['query_dropout'],
            mem_maskout=opt['mem_maskout'],
            dist_method=opt['dist_method'],
            mem_select_topk=mem_select_topk,
            mem_select_topk_type=opt['mem_select_topk_type'],
            mem_select_topk_tau=opt['mem_select_topk_tau'],
            mem_return_topk=opt['mem_return_topk'],
            mem_return_query=opt['mem_return_query'],
            scale_mutual_prox=opt['scale_mutual_prox'],
            mem_write_topk=opt['mem_write_topk'],
            mem_write_used_thresh=opt['mem_write_used_thresh'],
            mem_write_age_thresh=opt['mem_write_age_thresh'],
            mem_write_age_thresh_schedule=age_schedule,
            mem_write_vals=opt['mem_write_vals'],
            mem_dropout=opt['mem_dropout'],
            mem_result_scale_to=opt['mem_result_scale_to'],
            query_mem_locality_loss=opt['query_mem_locality_loss'],
            enc_mem_combine=opt['enc_mem_combine'],
            enc_mem_alpha=opt['enc_mem_alpha'],
            enc_mem_alpha_rand=opt['enc_mem_alpha_rand'],
            enc_mem_dropout=opt['enc_mem_dropout'],
            use_enc_mem_layernorm=opt['use_enc_mem_layernorm'],
            use_extra_enc_layer=opt['use_extra_enc_layer'],
            writer=self.writer,
            writer_name=self.writer_name
            )
        self.decoder = _build_trsfrmr_mem_decoder(
            opt, dictionary, self.embeddings, self.pad_idx,
            n_positions=n_positions,
            )

    def reorder_encoder_states(self, encoder_states, indices):
        enc, mask = encoder_states
        if not torch.is_tensor(indices):
            indices = torch.LongTensor(indices).to(enc.device)
        enc = torch.index_select(enc, 0, indices)
        mask = torch.index_select(mask, 0, indices)
        return enc, mask

    def reorder_decoder_incremental_state(self, incremental_state, inds):
        """No support for incremental decoding at this time"""
        return None

    def output(self, tensor):
        """Project back to vocabulary"""
        output = F.linear(tensor, self.embeddings.weight)
        return output

    def forward(
        self, *xs, ys=None, cand_params=None, prev_enc=None, maxlen=None, bsz=None
    ):
        """
        Get output predictions from the model.
        Overrides TorchGeneratorModel's forward. Key difference is to pass ys to encoder
        in order to write encoded targets to memory values.
        """
        if ys is not None:
            # TODO: get rid of longest_label
            # keep track of longest label we've ever seen
            # we'll never produce longer ones than that during prediction
            self.longest_label = max(self.longest_label, ys.size(1))

        # Encoding
        # use cached encoding if available
        if prev_enc is not None:
            encoder_states = prev_enc
        else:
            if ys is not None:
                encoder_states = self.encoder(*xs, targets=ys)
            else:
                encoder_states = self.encoder(*xs)

        # Decoding
        if ys is not None:
            # use teacher forcing
            scores, preds = self.decode_forced(encoder_states, ys)
        else:
            scores, preds = self.decode_greedy(
                encoder_states, bsz, maxlen or self.longest_label
            )

        return scores, preds, encoder_states

class TransformerGenMemBasicAgent(tsfrmr.TransformerGeneratorAgent):
    def __init__(self, opt, shared=None):
        super(TransformerGenMemBasicAgent, self).__init__(opt, shared)
        self.custom_metrics = {}
        self.infer_top1mems = set()  # tracks memories selected during inference
        self.infer_topmems = set()
        self.infer_nexs = 0

    @classmethod
    def add_cmdline_args(cls, argparser):
        super(TransformerGenMemBasicAgent, cls).add_cmdline_args(argparser)

        agent = argparser.add_argument_group('TransformerGenMemBasicAgent')

        agent.add_argument(
            '--tensorboard-log', type='bool', default=True,
            help='Track values of interest in tensorboard. Currently tracks '
                 'usage of memory slots.'
        )

        agent.add_argument(
            '--init-tsfrmr-model', type=str, default=None,
            help='Model to load transformer encoder and decoder weights from'
        )
        agent.add_argument(
            '--freeze-all-but-mem', type='bool', default=False,
            help='Freeze encoder and decoder. Probably used with --init-trsfrmr-model.'
        )

        agent.add_argument(
            '-msz', '--mem-size', type=int, default=1000,
            help='Size of memory.'
        )
        agent.add_argument(
            '-mdim', '--mem-dim', type=int, default=512,
            help='Dimension of embeddings in memory.'
        )
        agent.add_argument(
            '--use-product-keys', type='bool', default=False,
            help='Use product keys for memory.'
        )
        agent.add_argument(
            '--n-queries', type=int, default=1,
            help='Number of queries (and query networks). '
                 'Should be 1 or the same number as the number of heads.'
        )
        agent.add_argument(
            '--n-queries-write', type=str, default='first',
            help='When --n-queries > 1 and writing to memory, we have to choose which of '
                 'the queries to write to the keys. When "first", just use the first query '
                 '(i.e. it is deterministic). When "random", randomly select one of the '
                 'queries.'
        )
        agent.add_argument(
            '--query-network', type=str, default='lin_nobn',
            help='Type of network for converting context into memory query. '
                 'Options: lin_nobn, lin_bn, ffn'
        )
        agent.add_argument(
            '--query-dropout', type=float, default=0.0,
            help='Dropout on query to memory.'
        )
        agent.add_argument(
            '--mem-maskout', type=float, default=0.0,
            help='"Maskout" portions of the memory, i.e. only compute similarity of queries '
                 'against subset of the memories (different subset every forward pass). '
                 'Similar to dropout, when equal to 0, acts in the standard way: all memories '
                 'are used.'
        )

        agent.add_argument(
            '-dist', '--dist-method', type=str, default='cos',
            help='Calculate distances between (projected) queries and memory keys using .'
                 'dist product ("dist") or cosine similarity ("cos").'
        )

        agent.add_argument(
            '--mem-select-topk', type=str, default='-1',
            help='If value is > 0, instead of taking a softmax over all query-key '
                 'similarities, we use the top k most similar memories (see the following '
                 'argument for more details). '
                 'If value is a comma-separated list of values, then at every batch, we '
                 'randomly select one of the values.'
        )
        agent.add_argument(
            '--mem-select-topk-type', type=str, default='top',
            help='When "gumbel", use the gumbel_softmax_topk trick to set the '
                 'top k most similar memories as 1, rest as 0. '
                 'When "top", take the top k items according to the dist product. '
                 'Zero out everything else, then take the softmax.'
        )
        agent.add_argument(
            '--mem-select-topk-tau', type=float, default=1.0,
            help='Temperature to use with gumbel in mem-select-topk.'
        )

        agent.add_argument(
            '--mem-return-topk', type=int, default=-1,
            help='If value > 0, instead of blending memories, return the top k memories. '
                 'This must be used with --enc-mem-combine=append. The top k memories (values) '
                 'are then appended.'
        )

        agent.add_argument(
            '--mem-return-query', type='bool', default=False,
            help='Used for testing / debugging.'
        )

        agent.add_argument(
            '--scale-mutual-prox', type='bool', default=False,
            help='Scale distances bertween query and memory keys by mutual proximity.'
        )

        agent.add_argument(
            '--mem-write-topk', type='bool', default=False,
            help='Write to memory. Memory slot is used based on whether memory is found in '
                 'topk matches. Currently, must be used with --mem-select-topk-type="top".'
        )
        agent.add_argument(
            '--mem-write-used-thresh', type=float, default=-1,
            help='If > 0, write to memory. Threshold for whether a memory is used or not.'
        )
        agent.add_argument(
            '--mem-write-age-thresh-schedule', type=str, default=None,
            help='Pass in a hard-coded schedule of at what number of forward passes to increase '
                 'the age threshold. In format "step0:age0,step1:age1", e.g. "10000:1000,300000:10000".'
        )
        agent.add_argument(
            '--mem-write-age-thresh', type=int, default=-1,
            help='Threshold for how recently memory slot was used when writing. '
                 'Only write to slot if last used <thresh> steps ago.'
        )
        agent.add_argument(
            '--mem-write-vals', type='bool', default=False,
            help='Write query to memory values'
        )

        agent.add_argument(
            '--mem-result-scale-to', type=float, default=None,
            help='Scale memory result. Used during inference. Use case: model is trained with '
                 '--mem-select-topk=10, but we want to do inference with k=1. Empirically (and '
                 'theoretically, the norm with k=10 will be smaller. In this case, first eval '
                 'with k=10, look at the norm in the metrics, then run with this argument set '
                 'to that norm and k=1.'
        )

        agent.add_argument(
            '--mem-dropout', type=float, default=0.0,
            help='Dropout on memory result.'
        )
        agent.add_argument(
            '--query-mem-locality-loss', type='bool', default=False,
            help='Add loss that constrains pairwise similarities of memory results to be '
                 'similar to pairwise similarites of queries.'
        )
        agent.add_argument(
            '--query-mem-locality-loss-lambda', type=float, default=1.0,
            help='Weight on additional loss.'
        )

        agent.add_argument(
            '--enc-mem-combine', type=str, default='sum',
            help='Method to combine encoder outputs and memory result. "sum" or "append"'
        )
        agent.add_argument(
            '--enc-mem-alpha', type=float, default=0.5,
            help='Weight to combine encoder outputs and memory result. '
                 'An alpha of 1.0 means use only the encoded outputs; 0.0 only the memory result. '
                 'When enc_mem_combine=sum, this takes the weighted average of the two. '
                 'When enc_mem_combine=append, this value determines the binary mask. '
                 'With alpha=0.5, the mask is ones for both encoded and memory.'
        )
        agent.add_argument(
            '--enc-mem-alpha-rand', type='bool', default=False,
            help='Instead of using enc_mem_alpha to weight, draw from Uniform(0,1) to get '
                 'weights (that sum to 1).'
        )
        agent.add_argument(
            '--enc-mem-dropout', type=float, default=0.0,
            help='If > 0.0, "dropout" either the encoded inputs or the memory result. '
                 'This overwrites the alphas from above.'
        )
        agent.add_argument(
            '--use-enc-mem-layernorm', type='bool', default=False,
            help='Use layer norm after combining context and memory.'
        )
        agent.add_argument(
            '--use-extra-enc-layer', type='bool', default=False,
            help='Use extra Transformer encoder layer after combining context and memory.'
        )

        agent.add_argument(
            '--freeze-mem-keys-nexs', type=int, default=-1,
            help='If > 0, freeze the memory keys after n training examples.'
        )

        agent.add_argument(
            '--dec-zeroout', type=float, default=0.0,
            help='Do not use input embeddings during decoding, only positional embeddings.'
        )
        agent.add_argument(
            '--dec-maskout', type=float, default=0.0,
            help='Mask out previous embeddings. This is orthogonal to --dec-zeroout.'
        )

        return agent

    def build_model(self):
        self.model = TransformerGenMemBasicModel(self.opt, self.dict)
        if self.opt['embedding_type'] != 'random':
            # Copying embeddings is slow. Only do so when training. Otherwise, weights
            # will be loaded after build_model() is called
            if (self.opt['datatype'].startswith('train')) and \
                (not self.opt['datatype'].startswith('train:evalmode')):
                self._copy_embeddings(
                    self.model.tsfrmr_encoder.embeddings.weight, self.opt['embedding_type']
                )
        if self.use_cuda:
            self.model.cuda()

        # Load transformer encoder and decoder weights
        if self.opt['init_tsfrmr_model']:
            print('Loading pre-trained transformer model: {}'.format(
                self.opt['init_tsfrmr_model']))

            model_path = modelzoo_path(None, self.opt['init_tsfrmr_model'])
            states = torch.load(model_path, map_location=lambda cpu, _: cpu)

            if 'model' in states:
                # Rewrite encoder keys to match keys in our model
                updated_model_dict = OrderedDict()
                for name, param in states['model'].items():
                    if name.startswith('encoder'):
                        name = name.replace('encoder', 'tsfrmr_encoder')
                    updated_model_dict[name] = param

                # Strict = false because our model has parameters not found
                # in the pre-trained transformer
                self.model.load_state_dict(updated_model_dict, strict=False)

        if self.opt['freeze_all_but_mem']:
            # Freeze encoder and memory keys
            for param in self.model.tsfrmr_encoder.parameters():
                param.requires_grad = False
            for param in self.model.decoder.parameters():
                param.requires_grad = False

        return self.model

    def state_dict(self):
        """Save variables in Memory used for writing to memory."""
        states = super().state_dict()
        try:
            states['mem_used'] = self.model.encoder.memory.used
            states['mem_last_used'] = self.model.encoder.memory.last_used
            states['n_forwards'] = self.model.encoder.memory.n_forwards
        except Exception as e:
            states['mem_used'] = self.model.module.encoder.memory.used
            states['mem_last_used'] = self.model.module.encoder.memory.last_used
            states['n_forwards'] = self.model.module.encoder.memory.n_forwards
        return states

    def load(self, path):
        """
        Load and set variables in Memory used for writing to memory.

        TODO: need to check if this loads for all workers in distributed training.
        """
        states = super().load(path)
        try:
            self.model.encoder.memory.used = states['mem_used']
            self.model.encoder.memory.last_used = states['mem_last_used']
            self.model.encoder.memory.n_forwards = states['n_forwards']
        except AttributeError as e:
            self.model.module.encoder.memory.used = states['mem_used']
            self.model.module.encoder.memory.last_used = states['mem_last_used']
            self.model.module.encoder.memory.n_forwards = states['n_forwards']
        except KeyError as e:  # backwards compatability: earlier models didn't save the above
            pass

        return states

    def train_step(self, batch):
        """Train on a single batch of examples."""
        super(TransformerGenMemBasicAgent, self).train_step(batch)

        n_examples_done = self._number_training_updates * self.opt['batchsize']
        if self.opt['freeze_mem_keys_nexs'] > 0:
            if n_examples_done > self.opt['freeze_mem_keys_nexs']:
                self.model.encoder.memory.keys.requires_grad = False

    def reset_metrics(self):
        """Reset variables that are used during eval_step() to track memory usage."""
        super().reset_metrics()
        self.infer_top1mems = set()
        self.infer_topmems = set()
        self.infer_nexs = 0

    def eval_step(self, batch):
        output = super(TransformerGenMemBasicAgent, self).eval_step(batch)

        # Add custom metrics (track if different memories are being selected)
        topk_indices = None
        mem_result = None
        try:
            topk_indices = self.model.encoder.memory.topk_indices
            mem_result = self.model.encoder.mem_result
        except Exception as e:  # on valid during distributed training
            topk_indices = self.model.module.encoder.memory.topk_indices
            mem_result = self.model.module.encoder.mem_result

        if topk_indices is not None:
            top1 = topk_indices[:, 0].tolist()
            top = topk_indices.view(-1).tolist()
            self.infer_top1mems = self.infer_top1mems.union(set(top1))
            self.infer_topmems = self.infer_topmems.union(set(top))
            self.infer_nexs += batch['text_vec'].size(0)

            perc_unique_top1_mems = len(self.infer_top1mems) / float(self.infer_nexs) * 100
            perc_mems_used = len(self.infer_topmems) / float(self.opt['mem_size']) * 100
            self.custom_metrics['perc_unique_top1_mems'] = perc_unique_top1_mems
            self.custom_metrics['perc_mems_used'] = perc_mems_used

        if mem_result is not None:
            if 'mem_result_norm' not in self.custom_metrics:
                self.custom_metrics['mem_result_norm'] = []
            norm = mem_result.norm(dim=1).mean().item()
            self.custom_metrics['mem_result_norm'].append(norm)

        return output

    def report(self):
        """Add custom metrics to report."""
        base_metrics = super(TransformerGenMemBasicAgent, self).report()
        mem_metrics = {
            k: round_sigfigs(np.mean(values))
            for k, values in self.custom_metrics.items()
        }
        return {**base_metrics, **mem_metrics}

    def compute_loss(self, batch, return_output=False):
        """Override TorchGeneratorModel's function, adding custom loss."""
        if not self.opt['query_mem_locality_loss']:
            return super(TransformerGenMemBasicAgent, self).compute_loss(batch, return_output)
        else:  # add custom losses
            result = super(TransformerGenMemBasicAgent, self).compute_loss(batch, return_output)
            loss = result[0] if return_output else result
            try:
                q_sims = self.model.encoder.memory.cosine_sim(self.model.encoder.mem_query)  # [bsz, bsz]
                mem_sims =self.model.encoder.memory.cosine_sim(self.model.encoder.mem_result)  # [bsz, bsz]
            except Exception as e:
                q_sims = self.model.module.encoder.memory.cosine_sim(self.model.module.encoder.mem_query)  # [bsz, bsz]
                mem_sims = self.model.module.encoder.memory.cosine_sim(self.model.module.encoder.mem_result)  # [bsz, bsz]
            q_sims = q_sims.triu(diagonal=1)
            mem_sims = mem_sims.triu(diagonal=1)
            # bsz = q_sims.size(0)
            # n_pairs = (bsz - 1) * bsz / 2  # (n * (n+1)) / 2
            qm_locality_loss = (q_sims - mem_sims).sum().abs()
            qm_locality_loss *= self.opt['query_mem_locality_loss_lambda']
            self.custom_metrics['qm_locality_loss'] = qm_locality_loss.item()
            loss += qm_locality_loss

            if return_output:
                model_output = result[1]
                return loss, model_output
            else:
                return loss
