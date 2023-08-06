#!/usr/bin/env python3
from torch import nn
import torch
from torch.autograd import Variable
from torch.nn import functional as F
from copy import deepcopy
import numpy as np


def mask_out(data, mask):
    return data.index_select(0, mask.nonzero().squeeze())


def normalize(data, p=2, dim=1, eps=1e-12):
    return data / torch.norm(data, p, dim).clamp(min=eps).expand_as(data)


class Memory(object):
    def __init__(self, opt):
        self.opt = opt

        self.memory_keys = torch.zeros(opt['mem_size'], opt['rnn_h'])
        self.memory_values = torch.zeros(opt['mem_size'])
        self.memory_ages = torch.zeros(opt['mem_size'])
        self.recent_idxs = torch.zeros(2).long()
        self.alpha = 0.1
        self.softmax_temp = max(1.0, np.log(0.2 * opt['mem_knn']) / self.alpha)
        self.age_noise = 8.0

        if opt['cuda']:
            self.memory_keys = self.memory_keys.cuda()
            self.memory_values = self.memory_values.cuda()
            self.memory_ages = self.memory_ages.cuda()
            self.recent_idxs = self.recent_idxs.cuda()

    def query(self, query_keys, query_values=None, query_masks=None):
        """
        query_keys: [batch, mem_dim]
        query_values: [batch]
        query_masks: [batch], binary
        """
        opt = self.opt

        batch_size, mem_knn = query_keys.size(0), opt['mem_knn']

        #### using variables
        norm_query_keys = normalize(query_keys)  # [batch, mem_dim]
        similarities = torch.mm(
            norm_query_keys, Variable(self.memory_keys).transpose(0, 1)
        )  # [batch, mem_size]
        topk_sims, topk_idxs = torch.topk(
            similarities, mem_knn
        )  # [batch, k], [batch, k]
        softmax_alpha = F.softmax(topk_sims * self.softmax_temp)  # [batch, k]
        topk_values = (
            Variable(self.memory_values)
            .index_select(0, topk_idxs.view(-1))
            .view(batch_size, -1)
            .detach()
        )  # [batch, k]
        return_values = (softmax_alpha * topk_values).sum(1)  # [batch]

        if query_values is None:
            return return_values, None

        #### using tensors
        topk_idxs = topk_idxs.data
        topk_idxs = torch.cat(
            [topk_idxs, self.recent_idxs.unsqueeze(0).expand(batch_size, 2)], dim=1
        )  # [batch, k+2]
        topk_values = self.memory_values.index_select(0, topk_idxs.view(-1)).view(
            batch_size, -1
        )  # [batch, k+2]
        correct = torch.eq(
            topk_values, query_values.data.unsqueeze(1).expand_as(topk_values)
        ).float()  # [batch, k+2]
        first_correct = torch.max(correct, dim=1)[1].squeeze(1)  # [batch] 0..k+1
        first_wrong = torch.min(correct, dim=1)[1].squeeze(1)  # [batch] 0..k+1
        offset = torch.arange(0, batch_size).long() * (
            mem_knn + 2
        )  # [batch] 0*(k+2), 1*(k+2), ...
        correct_idxs = topk_idxs.view(-1).index_select(
            0, first_correct + offset
        )  # [batch], global indices
        wrong_idxs = topk_idxs.view(-1).index_select(
            0, first_wrong + offset
        )  # [batch], global indices
        correct_keys = self.memory_keys.index_select(
            0, correct_idxs
        )  # [batch, mem_dim]
        wrong_keys = self.memory_keys.index_select(0, wrong_idxs)  # [batch, mem_dim]
        first_correct_indicator = correct[:, 0]  # [batch]

        #### using variables
        correct_keys_var, wrong_keys_var = Variable(correct_keys), Variable(wrong_keys)
        if query_masks is not None:
            teacher_loss = (
                F.relu(
                    (wrong_keys_var * norm_query_keys).sum(1)
                    - (correct_keys_var * norm_query_keys).sum(1)
                    + self.alpha
                )
                * query_masks
            ).sum() / query_masks.sum()
        else:
            teacher_loss = F.relu(
                (wrong_keys_var * norm_query_keys).sum(1)
                - (correct_keys_var * norm_query_keys).sum(1)
                + self.alpha
            ).mean()

        #### using tensors
        update_idxs_correct = correct_idxs  # [batch]
        noise = torch.zeros(opt['mem_size']).uniform_(-self.age_noise, self.age_noise)
        mem_noisy_ages = self.memory_ages + noise  # [mem_size]
        _, update_idxs_wrong = torch.topk(
            mem_noisy_ages, batch_size, 0, sorted=False
        )  # [batch]
        update_idxs = (
            update_idxs_correct.float() * first_correct_indicator
            + update_idxs_wrong.float() * (1 - first_correct_indicator)
        ).long()  # [batch]

        norm_query_keys_data = norm_query_keys.data
        update_keys_correct = normalize(
            correct_keys + norm_query_keys_data
        )  # [batch, mem_dim]
        update_keys_wrong = norm_query_keys_data  # [batch, mem_dim]
        indicator_exp = first_correct_indicator.unsqueeze(1).expand_as(
            update_keys_correct
        )
        update_keys = update_keys_correct * (indicator_exp) + update_keys_wrong * (
            1 - indicator_exp
        )  # [batch, mem_dim]

        update_idxs_exp = update_idxs.unsqueeze(1).expand_as(
            update_keys
        )  # [batch, mem_dim]
        query_values_data = query_values.data  # [batch]

        if query_masks is not None:
            query_masks_data = query_masks.data
            update_idxs_exp = mask_out(update_idxs_exp, query_masks_data)
            update_idxs = mask_out(update_idxs, query_masks_data)
            update_keys = mask_out(update_keys, query_masks_data)
            query_values_data = mask_out(query_values_data, query_masks_data)

        self.memory_keys.scatter_(0, update_idxs_exp, update_keys)
        self.memory_values.scatter_(0, update_idxs, query_values_data)
        self.memory_ages.add_(1.0)
        self.memory_ages.scatter_(0, update_idxs, 0.0)

        _, first_pos = torch.max(query_values_data, dim=0)  # [1]
        _, first_neg = torch.min(query_values_data, dim=0)  # [1]
        self.recent_idxs[0] = update_idxs[first_pos[0]]
        self.recent_idxs[1] = update_idxs[first_neg[0]]

        return return_values, teacher_loss


class ObjectChecklistModel(nn.Module):
    def __init__(self, opt, data_agent):
        super().__init__()
        self.opt = opt

        self.input_emb = nn.Embedding(
            data_agent.wordcnt, opt['embedding_dim'], padding_idx=0
        )
        self.action_type_emb = nn.Embedding(
            data_agent.get_num_actions(), opt['action_type_emb_dim']
        )
        self.encoder = nn.GRU(
            opt['embedding_dim'],
            opt['rnn_h'],
            opt['rnn_layers'],
            batch_first=True,
            bidirectional=opt['bidir'],
        )
        self.decoder = nn.Sequential(
            nn.Linear(opt['rnn_h'] + (1 if opt['memnet'] else 0), 1)
        )
        self.check_predictor = nn.Sequential(
            nn.Linear(
                opt['rnn_h'] * (2 if opt['bidir'] else 1)
                + opt['action_type_emb_dim']
                + opt['rnn_h'],
                opt['rnn_h'],
            ),
            nn.Tanh(),
            nn.Linear(opt['rnn_h'], 1),
            nn.Sigmoid(),
        )
        self.log_softmax = nn.LogSoftmax()
        self.trans = nn.Sequential(
            nn.Linear(opt['rnn_h'] * (2 if opt['bidir'] else 1), opt['embedding_dim']),
            nn.Tanh(),
        )
        self.dec_gru = nn.GRU(
            opt['rnn_h'] * (2 if opt['bidir'] else 1)
            + (opt['counter_emb_dim'] if opt['use_counter_feat'] else 1)
            + opt['embedding_dim']
            + opt['action_type_emb_dim']
            + opt['action_type_emb_dim']
            + opt['embedding_dim']
            + (opt['embedding_dim'] if opt['y_in'] else 0)
            + opt['rnn_h'] * (2 if opt['bidir'] else 1)
            if opt['second_attention']
            else 0,
            opt['rnn_h'],
            opt['rnn_layers'],
            batch_first=True,
        )
        self.attn_net = nn.Sequential(
            nn.Linear(
                opt['rnn_h'] * (3 if opt['bidir'] else 2) + opt['embedding_dim'] * 2,
                opt['rnn_h'],
            ),
            nn.Tanh(),
            nn.Linear(opt['rnn_h'], 1),
        )
        self.merge = nn.Sequential(nn.Linear(opt['rnn_h'] * 2, opt['rnn_h']), nn.Tanh())

        if opt['load_embedding']:
            pretrained_embedding = torch.load(opt['pretrain_model'])
            if opt['cuda']:
                pretrained_embedding = pretrained_embedding.cuda()
            self.input_emb.weight.data.copy_(pretrained_embedding)

        if opt['fix_embedding']:
            self.input_emb.weight.requires_grad = False

        self.counter_emb = nn.Embedding(opt['counter_max'] + 1, opt['counter_emb_dim'])

        if opt['memnet']:
            self.memory = Memory(opt)

    def forward_loss(
        self,
        x,
        action_key,
        second_action_key,
        action_type,
        current_room,
        checked,
        y,
        y_mask,
        counter_feat,
        write_memory=True,
    ):
        """
        x: [batch, seq_in], int
        action_key: [y_dim], int
        second_action_key: [y_dim], int
        action_type: [y_dim], int
        current_room: [batch, seq_out], int
        checked: [batch, seq_out + 1, y_dim], float, binary
        y: [batch, seq_out, y_dim], float, binary
        y_mask: [batch, seq_out, y_dim], float, binary
        counter_feat: [batch, seq_out, y_dim], int
        """

        opt = self.opt
        batch_size, seq_out, seq_in = x.size(0), y.size(1), x.size(1)
        h_0 = Variable(
            torch.zeros(
                opt['rnn_layers'] * (2 if opt['bidir'] else 1), batch_size, opt['rnn_h']
            )
        )
        if opt['cuda']:
            h_0 = h_0.cuda()

        emb_out = self.input_emb(x)  # [batch, seq_in, dim]
        enc_out, hidden = self.encoder(
            emb_out, h_0
        )  # [batch, seq_in, h], [layer, batch, h]

        action_emb_ori = self.input_emb(action_key.unsqueeze(1)).squeeze(
            1
        )  # [y_dim, dim]
        y_dim, emb_dim = action_emb_ori.size()
        action_emb = (
            action_emb_ori.unsqueeze(0)
            .expand(batch_size, y_dim, emb_dim)
            .transpose(1, 2)
        )  # [batch, dim, y_dim]

        second_action_emb_ori = self.input_emb(second_action_key.unsqueeze(1)).squeeze(
            1
        )  # [y_dim, dim]
        second_action_emb = (
            second_action_emb_ori.unsqueeze(0)
            .expand(batch_size, y_dim, emb_dim)
            .transpose(1, 2)
        )  # [batch, dim, y_dim]

        alpha = F.softmax(
            torch.bmm(emb_out, action_emb).transpose(1, 2).contiguous().view(-1, seq_in)
            + torch.bmm(
                self.trans(enc_out.view(batch_size * seq_in, -1)).view(
                    batch_size, seq_in, -1
                ),
                action_emb,
            )
            .transpose(1, 2)
            .contiguous()
            .view(-1, seq_in)
        )  # [batch * y_dim, seq_in]
        attention = torch.bmm(
            alpha.view(batch_size, y_dim, seq_in), enc_out
        )  # [batch, y_dim, h]

        if opt['second_attention']:
            second_alpha = F.softmax(
                torch.bmm(emb_out, second_action_emb)
                .transpose(1, 2)
                .contiguous()
                .view(-1, seq_in)
                + torch.bmm(
                    self.trans(enc_out.view(batch_size * seq_in, -1)).view(
                        batch_size, seq_in, -1
                    ),
                    second_action_emb,
                )
                .transpose(1, 2)
                .contiguous()
                .view(-1, seq_in)
            )
            second_attention = torch.bmm(
                second_alpha.view(batch_size, y_dim, seq_in), enc_out
            )  # [batch, y_dim, h]

        action_type_out_ori = self.action_type_emb(action_type)  # [y_dim, dim]
        action_type_out = action_type_out_ori.unsqueeze(0).expand(
            batch_size, y_dim, opt['action_type_emb_dim']
        )
        action_type_emb_dim = action_type_out.size(2)

        room_emb = self.input_emb(current_room)  # [batch, seq_out, emb_dim]

        loss, check_loss = 0, Variable(torch.zeros(1))
        if opt['cuda']:
            check_loss = check_loss.cuda()

        hidden = (
            self.merge(hidden.view(batch_size, -1))
            .unsqueeze(1)
            .expand(batch_size, y_dim, opt['rnn_h'])
            .contiguous()
            .view(1, batch_size * y_dim, -1)
        )

        teacher_loss = 0.0
        for i in range(seq_out):
            if not opt['use_counter_feat']:
                check_in = checked[:, i]
                check_in = check_in.unsqueeze(2)  # [batch, y_dim, 1]
            else:
                counter_in = self.counter_emb(counter_feat[:, i])  # [batch, y_dim, dim]
            room_in = room_emb[:, i].unsqueeze(1).expand(batch_size, y_dim, emb_dim)

            if i == 0:
                y_in = Variable(torch.zeros(batch_size, y_dim))
                if opt['cuda']:
                    y_in = y_in.cuda()
            else:
                y_in = y[:, i - 1]

            y_second_in = (
                torch.mm(y_in, second_action_emb_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, emb_dim)
            )  # [batch, y_dim, dim]
            y_type_in = (
                torch.mm(y_in, action_type_out_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, action_type_emb_dim)
            )  # [batch, y_dim, dim]
            y_in = (
                torch.mm(y_in, action_emb_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, emb_dim)
            )  # [batch, y_dim, dim]

            dec_in_list = [
                attention,
                counter_in if opt['use_counter_feat'] else check_in,
                room_in,
                action_type_out,
            ]
            if opt['y_in']:
                dec_in_list.append(y_type_in)
                dec_in_list.append(y_second_in)
                dec_in_list.append(y_in)
            if opt['second_attention']:
                dec_in_list.append(second_attention)
            dec_in = torch.cat(dec_in_list, 2)
            dec_out, hidden = self.dec_gru(
                dec_in.view(batch_size * y_dim, 1, -1), hidden
            )  # [batch * y_dim, 1, h], [1, batch * y_dim, h]

            dec_out = dec_out.squeeze(1)  # [batch * y_dim, h]
            if opt['memnet']:
                if write_memory:
                    memory_out, cur_teacher_loss = self.memory.query(
                        dec_out, y[:, i].view(-1), y_mask[:, i].view(-1)
                    )  # [batch * y_dim]
                else:
                    memory_out, cur_teacher_loss = self.memory.query(
                        dec_out, query_masks=y_mask[:, i].view(-1)
                    )  # [batch * y_dim]
                dec_out = torch.cat([dec_out, memory_out], 1)
                if cur_teacher_loss is not None:
                    teacher_loss += cur_teacher_loss

            dec_out = self.log_softmax(self.decoder(dec_out).view(batch_size, y_dim))

            if not opt['y_mask']:
                loss += -(dec_out * y[:, i]).sum()
            else:
                loss += -(dec_out * y[:, i] * y_mask[:, i]).sum()

            if not opt['use_counter_feat']:
                check_in_cat = torch.cat(
                    [
                        attention.view(batch_size * y_dim, -1),
                        action_type_out.view(batch_size * y_dim, -1),
                        hidden.squeeze(0),
                    ],
                    1,
                )
                check_out = self.check_predictor(check_in_cat).view(batch_size, y_dim)
                check_loss += (
                    -(
                        (
                            checked[:, i + 1] * torch.log(check_out)
                            + (1 - checked[:, i + 1]) * torch.log(1 - check_out)
                        )
                        * y[:, i]
                    ).sum()
                    * opt['check_weight']
                )

        if not opt['y_mask']:
            loss /= y.sum()
        else:
            loss /= (y * y_mask).sum()
        check_loss /= y.sum()
        loss += teacher_loss / seq_out

        return loss + check_loss, loss, check_loss

    def forward_predict(
        self,
        x,
        action_key,
        second_action_key,
        action_type,
        check_mapping,
        checked,
        graphs,
        data_agent,
    ):
        """
        check_mapping: [y_dim, y_dim], float, binary
        """

        from .agents import DataAgent

        graphs = deepcopy(graphs)
        opt = self.opt
        batch_size, seq_out, seq_in = x.size(0), opt['max_seq_out'], x.size(1)
        h_0 = Variable(
            torch.zeros(
                opt['rnn_layers'] * (2 if opt['bidir'] else 1), batch_size, opt['rnn_h']
            ),
            volatile=True,
        )
        if opt['cuda']:
            h_0 = h_0.cuda()

        emb_out = self.input_emb(x)
        enc_out, hidden = self.encoder(emb_out, h_0)

        action_emb_ori = self.input_emb(action_key.unsqueeze(1)).squeeze(
            1
        )  # [y_dim, dim]
        y_dim, emb_dim = action_emb_ori.size()
        action_emb = (
            action_emb_ori.unsqueeze(0)
            .expand(batch_size, y_dim, emb_dim)
            .transpose(1, 2)
        )  # [batch, dim, y_dim]

        second_action_emb_ori = self.input_emb(second_action_key.unsqueeze(1)).squeeze(
            1
        )  # [y_dim, dim]
        second_action_emb = (
            second_action_emb_ori.unsqueeze(0)
            .expand(batch_size, y_dim, emb_dim)
            .transpose(1, 2)
        )  # [batch, dim, y_dim]

        alpha = F.softmax(
            torch.bmm(emb_out, action_emb).transpose(1, 2).contiguous().view(-1, seq_in)
            + torch.bmm(
                self.trans(enc_out.view(batch_size * seq_in, -1)).view(
                    batch_size, seq_in, -1
                ),
                action_emb,
            )
            .transpose(1, 2)
            .contiguous()
            .view(-1, seq_in)
        )
        attention = torch.bmm(
            alpha.view(batch_size, y_dim, seq_in), enc_out
        )  # [batch, y_dim, h]

        if opt['second_attention']:
            second_alpha = F.softmax(
                torch.bmm(emb_out, second_action_emb)
                .transpose(1, 2)
                .contiguous()
                .view(-1, seq_in)
                + torch.bmm(
                    self.trans(enc_out.view(batch_size * seq_in, -1)).view(
                        batch_size, seq_in, -1
                    ),
                    second_action_emb,
                )
                .transpose(1, 2)
                .contiguous()
                .view(-1, seq_in)
            )
            second_attention = torch.bmm(
                second_alpha.view(batch_size, y_dim, seq_in), enc_out
            )  # [batch, y_dim, h]

        action_type_out_ori = self.action_type_emb(action_type.unsqueeze(1)).squeeze(
            1
        )  # [y_dim, dim]
        action_type_out = action_type_out_ori.unsqueeze(0).expand(
            batch_size, y_dim, opt['action_type_emb_dim']
        )
        action_type_emb_dim = action_type_out.size(2)

        if not opt['use_counter_feat']:
            check_in = Variable(torch.zeros(batch_size, y_dim), volatile=True)
            if opt['cuda']:
                check_in = check_in.cuda()
        else:
            counter_feat = Variable(torch.zeros(batch_size, y_dim).long())
            if opt['cuda']:
                counter_feat = counter_feat.cuda()

        text_out = [[] for _ in range(batch_size)]

        hidden = (
            self.merge(hidden.view(batch_size, -1))
            .unsqueeze(1)
            .expand(batch_size, y_dim, opt['rnn_h'])
            .contiguous()
            .view(1, batch_size * y_dim, -1)
        )

        for i in range(seq_out):
            room_in = torch.zeros(batch_size).long()
            for j in range(batch_size):
                room_in[j] = data_agent.get_room(graphs[j])
            if opt['cuda']:
                room_in = room_in.cuda()
            room_in = Variable(room_in, volatile=True)
            room_in = self.input_emb(room_in.unsqueeze(1)).expand(
                batch_size, y_dim, emb_dim
            )

            if i == 0:
                y_in = Variable(torch.zeros(batch_size, y_dim))
                if opt['cuda']:
                    y_in = y_in.cuda()
            else:
                y_in = y_onehot

            y_second_in = (
                torch.mm(y_in, second_action_emb_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, emb_dim)
            )  # [batch, y_dim, dim]
            y_type_in = (
                torch.mm(y_in, action_type_out_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, action_type_emb_dim)
            )  # [batch, y_dim, dim]
            y_in = (
                torch.mm(y_in, action_emb_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, emb_dim)
            )  # [batch, y_dim, dim]

            if opt['use_counter_feat']:
                counter_in = self.counter_emb(counter_feat)  # [batch, y_dim, dim]

            dec_in_list = [
                attention,
                counter_in if opt['use_counter_feat'] else check_in.unsqueeze(2),
                room_in,
                action_type_out,
            ]
            if opt['y_in']:
                dec_in_list.append(y_type_in)
                dec_in_list.append(y_second_in)
                dec_in_list.append(y_in)
            if opt['second_attention']:
                dec_in_list.append(second_attention)
            dec_in = torch.cat(dec_in_list, 2)

            dec_out, hidden = self.dec_gru(
                dec_in.view(batch_size * y_dim, 1, -1), hidden
            )  # [batch * y_dim, 1, h], [1, batch * y_dim, h]

            y_mask = torch.zeros(batch_size, y_dim)
            for j in range(batch_size):
                data_agent.get_mask(graphs[j], y_mask[j])
            if opt['cuda']:
                y_mask = y_mask.cuda()
            y_mask = Variable(y_mask, volatile=True)

            dec_out = dec_out.squeeze(1)  # [batch * y_dim, h]
            if opt['memnet']:
                memory_out, _ = self.memory.query(
                    dec_out, query_masks=y_mask.view(-1)
                )  # [batch * y_dim]
                dec_out = torch.cat([dec_out, memory_out], 1)

            dec_out = self.decoder(dec_out).view(batch_size, y_dim)

            if not opt['use_counter_feat']:
                check_in_cat = torch.cat(
                    [
                        attention.view(batch_size * y_dim, -1),
                        action_type_out.view(batch_size * y_dim, -1),
                        hidden.squeeze(0),
                    ],
                    1,
                )
                check_out = self.check_predictor(check_in_cat).view(batch_size, y_dim)
                check_out = torch.ge(check_out, 0.5).float()

            dec_out = dec_out * y_mask + -1e7 * (1 - y_mask)
            y_out = torch.max(dec_out, 1)[1].data
            y_onehot = torch.zeros(batch_size, y_dim)
            y_onehot.scatter_(1, y_out.cpu(), 1)
            if opt['cuda']:
                y_onehot = y_onehot.cuda()
            y_onehot = Variable(y_onehot, volatile=True)  # [batch, y_dim]

            if not opt['use_counter_feat']:
                check_out = torch.mm(check_out * y_onehot, check_mapping)
                check_in = torch.max(check_out, check_in)

            y_out = y_out.squeeze()
            for j in range(batch_size):
                if len(text_out[j]) > 0 and text_out[j][-1] == 'STOP':
                    continue
                cur_tuple = data_agent.get_action_tuple(y_out[j])
                text_out[j].append(data_agent.reverse_parse_action(cur_tuple))
                if text_out[j][-1] != 'STOP':
                    assert graphs[j].parse_exec(text_out[j][-1]), text_out[j][-1]

                    if opt['use_counter_feat']:
                        for action_name in data_agent.key_to_check[
                            data_agent.check_to_key[cur_tuple]
                        ]:
                            action_id = data_agent.get_action_id(action_name)
                            counter_feat[j, action_id] = counter_feat[j, action_id] + 1
                        counter_feat.data.clamp_(max=opt['counter_max'])

        return text_out


class Seq2SeqModel(nn.Module):
    def __init__(self, opt, data_agent):
        super().__init__()
        self.opt = opt

        self.y_dim = data_agent.y_dim

        self.input_emb = nn.Embedding(
            data_agent.wordcnt, opt['embedding_dim'], padding_idx=0
        )
        self.encoder = nn.GRU(
            opt['embedding_dim'], opt['rnn_h'], opt['rnn_layers'], batch_first=True
        )
        self.decoder = nn.GRU(
            self.y_dim, opt['rnn_h'], opt['rnn_layers'], batch_first=True
        )
        self.mapping = nn.Sequential(
            nn.Linear(opt['rnn_h'] * 2, self.y_dim), nn.LogSoftmax()
        )

        self.criterion = nn.CrossEntropyLoss()

    def forward_loss(self, x, y):
        """
        x: [batch, seq_in], int
        y: [batch, seq_out, 3 * target], float, binary
        """

        opt = self.opt
        batch_size, seq_out = x.size(0), y.size(1)
        h_0 = Variable(torch.zeros(opt['rnn_layers'], batch_size, opt['rnn_h']))
        if opt['cuda']:
            h_0 = h_0.cuda()

        enc_out, hidden = self.encoder(
            self.input_emb(x), h_0
        )  # [batch, seq_in, h], [layer, batch, h]
        loss = 0
        for i in range(seq_out):
            if i == 0:
                y_in = Variable(torch.zeros(batch_size, 1, y.size(2)))
                if opt['cuda']:
                    y_in = y_in.cuda()
            else:
                y_in = y[:, i - 1].unsqueeze(1)
            dec_out, hidden = self.decoder(
                y_in, hidden
            )  # [batch, 1, h], [layer, batch, h]
            alpha = F.softmax(
                torch.bmm(enc_out, hidden[-1].unsqueeze(2))
            )  # [batch, seq_in, 1]
            attention = torch.bmm(enc_out.transpose(1, 2), alpha).squeeze(
                2
            )  # [batch, h]
            dec_out = self.mapping(
                torch.cat([attention, dec_out.squeeze(1)], dim=1)
            )  # [batch, y_dim]
            loss += -(dec_out * y[:, i]).sum()
        loss /= y.sum()

        return loss

    def forward_predict(self, x, graphs, data_agent):
        graphs = deepcopy(graphs)
        opt = self.opt
        batch_size = x.size(0)
        h_0 = Variable(torch.zeros(opt['rnn_layers'], batch_size, opt['rnn_h']))
        if opt['cuda']:
            h_0 = h_0.cuda()

        enc_out, hidden = self.encoder(
            self.input_emb(x), h_0
        )  # [batch, seq_in, h], [layer, batch, h]
        text_out = [[] for _ in range(batch_size)]
        for i in range(opt['max_seq_out']):
            if i == 0:
                y_in = Variable(torch.zeros(batch_size, 1, self.y_dim))
                if opt['cuda']:
                    y_in = y_in.cuda()
            else:
                y_in = y_onehot.unsqueeze(1)

            dec_out, hidden = self.decoder(y_in, hidden)
            alpha = F.softmax(torch.bmm(enc_out, hidden[-1].unsqueeze(2)))
            attention = torch.bmm(enc_out.transpose(1, 2), alpha).squeeze(2)
            dec_out = self.mapping(
                torch.cat([attention, dec_out.squeeze(1)], dim=1)
            )  # [batch, y_dim]

            y_mask = torch.zeros(batch_size, self.y_dim)
            for j in range(batch_size):
                data_agent.get_mask(graphs[j], y_mask[j])
            if opt['cuda']:
                y_mask = y_mask.cuda()
            y_mask = Variable(y_mask, volatile=True)
            dec_out = dec_out * y_mask + -1e7 * (1 - y_mask)

            y_out = torch.max(dec_out, 1)[1].data  # [batch, 1]
            y_onehot = torch.zeros(batch_size, self.y_dim)  # [batch, y_dim]
            y_onehot.scatter_(1, y_out.cpu(), 1)
            y_onehot = Variable(y_onehot)
            if opt['cuda']:
                y_onehot = y_onehot.cuda()

            y_out = y_out.squeeze()
            for j in range(batch_size):
                if len(text_out[j]) > 0 and text_out[j][-1] == 'STOP':
                    continue
                text_out[j].append(
                    data_agent.reverse_parse_action(
                        data_agent.get_action_tuple(y_out[j])
                    )
                )
                if text_out[j][-1] != 'STOP':
                    assert graphs[j].parse_exec(text_out[j][-1]), text_out[j][-1]
        return text_out
