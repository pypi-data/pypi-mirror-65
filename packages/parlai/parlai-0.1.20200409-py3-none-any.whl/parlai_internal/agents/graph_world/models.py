#!/usr/bin/env python3
from torch import nn
import torch
from torch.autograd import Variable
from torch.nn import functional as F
from copy import deepcopy
import numpy as np


class RuleDecoder(nn.Module):
    def __init__(self, opt, data_agent):
        super().__init__()
        self.opt = opt

        # self.weight_action = nn.Parameter(torch.Tensor(1, ))
        # self.weight_stop = nn.Parameter(torch.Tensor(1, ))
        # self.weight_action.data.zero_()
        # self.weight_stop.data.zero_()

        self.weight_action = 0.9
        self.weight_stop = 0.8

        self.criterion = nn.CrossEntropyLoss()

    def forward(self, x, map=None, y=None, loss=True, graphs=None):
        if loss:
            return self._forward_loss(x, map, y)
        else:
            return self._forward_predict(x, graphs)

    def _forward_loss(self, x, map, y):
        """
        x: [batch, seq_in], int
        map: [batch, seq_out, feat], float
        y: [batch, seq_out, y_dim], float, binary
        """
        from .agents import DataAgent

        opt = self.opt
        batch_size, seq_out = x.size(0), y.size(1)
        h_0 = torch.zeros(opt['rnn_layers'], batch_size, opt['rnn_h'])
        if opt['cuda']:
            h_0.cuda()
        h_0 = Variable(h_0)

        # enc_out, hidden = self.encoder(self.input_emb(x), h_0) # [batch, seq_in, h], [layer, batch, h]
        # enc_out, hidden = self.encoder(x, h_0)
        # hidden = self.encoder(x).unsqueeze(0)
        # hidden = h_0
        loss = 0
        for i in range(seq_out):
            # if i == 0:
            #     y_in = Variable(torch.zeros(batch_size, 1, y.size(2)))
            #     if opt['cuda']:
            #         y_in.cuda()
            # else:
            #     y_in = y[:, i - 1].unsqueeze(1)

            # dec_out, hidden = self.decoder(x[:, i].unsqueeze(1), hidden)
            # dec_out, hidden = self.decoder(torch.cat([map[:, i].unsqueeze(1), x[:, i].unsqueeze(1)], dim=2), hidden)
            # dec_out, hidden = self.decoder(torch.cat([map[:, i].unsqueeze(1), y_in, x[:, i].unsqueeze(1)], dim=2), hidden)

            # dec_out, hidden = self.decoder(torch.cat([map[:, i].unsqueeze(1), y_in], dim=2), hidden) # [batch, 1, h], [layer, batch, h]
            # alpha = F.softmax(torch.bmm(enc_out, hidden[-1].unsqueeze(2))) # [batch, seq_in, 1]
            # attention = torch.bmm(enc_out.transpose(1, 2), alpha).squeeze(2) # [batch, h]
            # dec_out = self.mapping(torch.cat([attention, dec_out.squeeze(1)], dim=1)) # [batch, y_dim]
            # dec_out = self.mapping(dec_out.squeeze(1))

            # dec_out = self.decoder(x[:, i])

            action_out_1 = x[:, i, : opt['num_objects']] * self.weight_action.expand(
                batch_size, opt['num_objects']
            )
            action_out_2 = x[:, i, : opt['num_objects']] * self.weight_action.expand(
                batch_size, opt['num_objects']
            )
            action_out_3 = x[:, i, opt['num_objects'] :] * self.weight_action.expand(
                batch_size, opt['num_rooms']
            )
            stop_out = self.weight_stop.unsqueeze(0).expand(batch_size, 1)
            dec_out = torch.cat([action_out_1, action_out_2, action_out_3, stop_out], 1)

            loss += -(dec_out * y[:, i]).sum()
        loss /= y.sum()

        return loss

    def _forward_predict(self, x, graphs):
        from .agents import DataAgent

        graphs = deepcopy(graphs)
        opt = self.opt
        batch_size = x.size(0)
        h_0 = torch.zeros(opt['rnn_layers'], batch_size, opt['rnn_h'])
        if opt['cuda']:
            h_0.cuda()
        h_0 = Variable(h_0, volatile=True)

        x = x.data.numpy()

        # enc_out, hidden = self.encoder(self.input_emb(x), h_0) # [batch, seq_in, h], [layer, batch, h]
        # enc_out, hidden = self.encoder(x, h_0)
        # hidden = self.encoder(x).unsqueeze(0)
        hidden = h_0
        text_out = [[] for _ in range(batch_size)]
        for i in range(opt['max_seq_out']):
            # if i == 0:
            #     y_in = Variable(torch.zeros(batch_size, 1, opt['y_dim']), volatile=True)
            #     if opt['cuda']:
            #         y_in.cuda()
            # else:
            #     y_in = y_onehot.unsqueeze(1)
            map = torch.zeros(batch_size, 1, opt['feat_dim'])
            for j in range(batch_size):
                DataAgent.get_map(graphs[j], map[j, 0])
            if opt['cuda']:
                map.cuda()
            map = Variable(map, volatile=True)

            # x_in = Variable(torch.from_numpy(x[:, i])).unsqueeze(1)
            x_in = torch.from_numpy(x[:, i])
            if opt['cuda']:
                x_in.cuda()
            x_in = Variable(x_in)

            # dec_out, hidden = self.decoder(x_in, hidden)
            # dec_out, hidden = self.decoder(torch.cat([map, x_in], dim=2), hidden)
            # dec_out, hidden = self.decoder(torch.cat([map, y_in, x_in], dim=2), hidden)

            # dec_out, hidden = self.decoder(torch.cat([map, y_in], dim=2), hidden)
            # alpha = F.softmax(torch.bmm(enc_out, hidden[-1].unsqueeze(2)))
            # attention = torch.bmm(enc_out.transpose(1, 2), alpha).squeeze(2)
            # dec_out = self.mapping(torch.cat([attention, dec_out.squeeze(1)], dim=1)) # [batch, y_dim]
            # dec_out = self.mapping(dec_out.squeeze(1))

            # dec_out = self.decoder(x_in)

            action_out_1 = (
                x_in[:, : opt['num_objects']] * self.weight_action
            )  # * self.weight_action.expand(batch_size, opt['num_objects'])
            action_out_2 = (
                x_in[:, : opt['num_objects']] * self.weight_action
            )  # .expand(batch_size, opt['num_objects'])
            action_out_3 = (
                x_in[:, opt['num_objects'] :] * self.weight_action
            )  # .expand(batch_size, opt['num_rooms'])
            # stop_out = self.weight_stop.unsqueeze(0).expand(batch_size, 1)
            stop_out = torch.Tensor(batch_size, 1).fill_(self.weight_stop)
            if opt['cuda']:
                stop_out.cuda()
            stop_out = Variable(stop_out)
            dec_out = torch.cat([action_out_1, action_out_2, action_out_3, stop_out], 1)

            all_one = torch.ones(batch_size, 1)
            if opt['cuda']:
                all_one.cuda()
            all_one = Variable(all_one)
            y_mask = torch.cat([map[:, 0], all_one], dim=1)  # [batch, y_dim]

            dec_out = dec_out * y_mask + -1e7 * (1 - y_mask)

            y_out = torch.max(dec_out, 1)[1].data  # [batch, 1]
            y_onehot = torch.zeros(batch_size, opt['y_dim'])  # [batch, y_dim]
            y_onehot.scatter_(1, y_out, 1)
            if opt['cuda']:
                y_onehot.cuda()
            y_onehot = Variable(y_onehot, volatile=True)

            y_out = y_out.squeeze()
            num_objects = opt['num_objects']
            for j in range(batch_size):
                if len(text_out[j]) > 0 and text_out[j][-1] == 'STOP':
                    continue
                g = graphs[j]
                if y_out[j] < num_objects:
                    inst_str = 'get {}'.format(g.objects[y_out[j]])
                elif y_out[j] < 2 * num_objects:
                    inst_str = 'drop {}'.format(g.objects[y_out[j] - num_objects])
                elif y_out[j] < opt['y_dim'] - 1:
                    inst_str = 'go {}'.format(g.rooms[y_out[j] - 2 * num_objects])
                else:
                    inst_str = 'STOP'
                text_out[j].append(inst_str)
                if inst_str != 'STOP':
                    assert g.parse_exec(inst_str), inst_str

                if inst_str != 'STOP' and i < opt['max_seq_out'] - 1:
                    DataAgent.update_x(g, inst_str, x[j, i], x[j, i + 1])
        return text_out


class ObjectChecklistModel(nn.Module):
    def __init__(self, opt, data_agent):
        super().__init__()
        self.opt = opt

        self.input_emb = nn.Embedding(
            data_agent.wordcnt, opt['embedding_dim'], padding_idx=0
        )
        self.action_type_emb = nn.Embedding(
            opt['num_actions'] + 1, opt['action_type_emb_dim']
        )
        self.encoder = nn.GRU(
            opt['embedding_dim'],
            opt['rnn_h'],
            opt['rnn_layers'],
            batch_first=True,
            bidirectional=opt['bidir'],
        )
        self.decoder = nn.Sequential(
            # nn.Linear(opt['rnn_h'] * (2 if opt['bidir'] else 1) + 1 + opt['embedding_dim'] + opt['action_type_emb_dim'], opt['rnn_h']),
            # nn.Tanh(),
            nn.Linear(opt['rnn_h'], 1)
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
        # self.init_check_predictor = nn.Sequential(
        #     nn.Linear(opt['action_type_emb_dim'] + 1, opt['action_type_emb_dim']),
        #     nn.Tanh(),
        #     nn.Linear(opt['action_type_emb_dim'], 1),
        #     nn.Sigmoid(),
        # )
        self.log_softmax = nn.LogSoftmax()
        self.trans = nn.Sequential(
            nn.Linear(opt['rnn_h'] * (2 if opt['bidir'] else 1), opt['embedding_dim']),
            nn.Tanh(),
        )
        self.dec_gru = nn.GRU(
            opt['rnn_h'] * (2 if opt['bidir'] else 1)
            + 1
            + opt['embedding_dim']
            + opt['action_type_emb_dim']
            + (opt['embedding_dim'] if opt['y_in'] else 0),
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

    def forward_loss(self, x, action_key, action_type, current_room, checked, y):
        """
        x: [batch, seq_in], int
        action_key: [y_dim], int
        action_type: [y_dim], int
        current_room: [batch, seq_out], int
        checked: [batch, seq_out + 1, y_dim], float, binary
        y: [batch, seq_out, y_dim], float, binary
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

        action_type_out = self.action_type_emb(action_type)  # [y_dim, dim]
        action_type_out = action_type_out.unsqueeze(0).expand(
            batch_size, y_dim, opt['action_type_emb_dim']
        )

        room_emb = self.input_emb(current_room)  # [batch, seq_out, emb_dim]

        loss, check_loss = 0, 0

        # check_in = torch.mm(room_emb[:, 0], action_emb[0]) # [batch, y_dim]
        # check_in = torch.cat([check_in.unsqueeze(2), action_type_out], 2)
        # check_in = self.init_check_predictor(check_in.view(batch_size * y_dim, -1)).view(batch_size, y_dim)
        # check_init_loss = - (checked[:, 0] * torch.log(check_in) + (1 - checked[:, 0]) * torch.log(1 - check_in)).sum() / batch_size / y_dim * opt['check_weight'] * 0.0

        hidden = (
            self.merge(hidden.view(batch_size, -1))
            .unsqueeze(1)
            .expand(batch_size, y_dim, opt['rnn_h'])
            .contiguous()
            .view(1, batch_size * y_dim, -1)
        )

        for i in range(seq_out):
            check_in = checked[:, i]
            check_in = check_in.unsqueeze(2)  # [batch, y_dim, 1]
            room_in = room_emb[:, i].unsqueeze(1).expand(batch_size, y_dim, emb_dim)

            if i == 0:
                y_in = Variable(torch.zeros(batch_size, y_dim))
                if opt['cuda']:
                    y_in = y_in.cuda()
            else:
                y_in = y[:, i - 1]

            y_in = (
                torch.mm(y_in, action_emb_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, emb_dim)
            )  # [batch, y_dim, dim]

            if opt['y_in']:
                dec_in = torch.cat(
                    [attention, check_in, room_in, action_type_out, y_in], 2
                )
            else:
                dec_in = torch.cat([attention, check_in, room_in, action_type_out], 2)
            # dec_out = self.log_softmax(self.decoder(dec_in.view(batch_size * y_dim, -1)).view(batch_size, y_dim)) # [batch, y_dim]
            dec_out, hidden = self.dec_gru(
                dec_in.view(batch_size * y_dim, 1, -1), hidden
            )  # [batch * y_dim, 1, h], [1, batch * y_dim, h]
            dec_out = self.log_softmax(
                self.decoder(dec_out.squeeze(1)).view(batch_size, y_dim)
            )

            loss += -(dec_out * y[:, i]).sum()

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

        loss /= y.sum()
        check_loss /= y.sum()

        return loss + check_loss, loss, check_loss

    def forward_predict(
        self, x, action_key, action_type, check_mapping, checked, graphs, data_agent
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

        action_type_out = self.action_type_emb(action_type.unsqueeze(1)).squeeze(
            1
        )  # [y_dim, dim]
        action_type_out = action_type_out.unsqueeze(0).expand(
            batch_size, y_dim, opt['action_type_emb_dim']
        )

        # check_in = self.init_check_predictor(attention.view(batch_size * y_dim, -1)).view(batch_size, y_dim)
        # check_in = torch.ge(check_in, 0.5).float()
        # check_in = checked[:, 0]
        check_in = Variable(torch.zeros(batch_size, y_dim), volatile=True)
        if opt['cuda']:
            check_in = check_in.cuda()

        # room_in = torch.zeros(batch_size).long()
        # for j in range(batch_size):
        #     room_in[j] = data_agent.get_room(graphs[j])
        # if opt['cuda']:
        #     room_in = room_in.cuda()
        # room_in = Variable(room_in, volatile=True)
        # room_in = self.input_emb(room_in.unsqueeze(1)).squeeze(1)
        # check_in = torch.mm(room_in, action_emb[0]) # [batch, y_dim]
        # check_in = torch.cat([check_in.unsqueeze(2), action_type_out], 2)
        # check_in = self.init_check_predictor(check_in.view(batch_size * y_dim, -1)).view(batch_size, y_dim)
        # check_in = torch.ge(check_in, 0.5).float()

        # check_in = checked[:, 0]

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

            y_in = (
                torch.mm(y_in, action_emb_ori)
                .unsqueeze(1)
                .expand(batch_size, y_dim, emb_dim)
            )  # [batch, y_dim, dim]

            if opt['y_in']:
                dec_in = torch.cat(
                    [attention, check_in.unsqueeze(2), room_in, action_type_out, y_in],
                    2,
                )
            else:
                dec_in = torch.cat(
                    [attention, check_in.unsqueeze(2), room_in, action_type_out], 2
                )

            # dec_out = self.decoder(dec_in.view(batch_size * y_dim, -1)).view(batch_size, y_dim) # does not need log softmax
            dec_out, hidden = self.dec_gru(
                dec_in.view(batch_size * y_dim, 1, -1), hidden
            )  # [batch * y_dim, 1, h], [1, batch * y_dim, h]
            dec_out = self.decoder(dec_out.squeeze(1)).view(batch_size, y_dim)

            check_in_cat = torch.cat(
                [
                    attention.view(batch_size * y_dim, -1),
                    action_type_out.view(batch_size * y_dim, -1),
                    hidden.squeeze(0),
                ],
                1,
            )
            check_out = self.check_predictor(check_in_cat).view(batch_size, y_dim)
            # check_out = self.check_predictor(attention.view(batch_size * y_dim, -1)).view(batch_size, y_dim) # [batch, y_dim]
            check_out = torch.ge(check_out, 0.5).float()

            y_mask = torch.zeros(batch_size, y_dim)
            for j in range(batch_size):
                DataAgent.get_mask(graphs[j], y_mask[j])
            if opt['cuda']:
                y_mask = y_mask.cuda()
            y_mask = Variable(y_mask, volatile=True)
            dec_out = dec_out * y_mask + -1e7 * (1 - y_mask)

            y_out = torch.max(dec_out, 1)[1].data
            y_onehot = torch.zeros(batch_size, y_dim)
            y_onehot.scatter_(1, y_out.cpu(), 1)
            if opt['cuda']:
                y_onehot = y_onehot.cuda()
            y_onehot = Variable(y_onehot, volatile=True)  # [batch, y_dim]

            check_out = torch.mm(check_out * y_onehot, check_mapping)
            check_in = torch.max(check_out, check_in)

            y_out = y_out.squeeze()
            num_objects = opt['num_objects']
            for j in range(batch_size):
                if len(text_out[j]) > 0 and text_out[j][-1] == 'STOP':
                    continue
                g = graphs[j]
                if y_out[j] < num_objects:
                    inst_str = 'get {}'.format(g.objects[y_out[j]])
                elif y_out[j] < 2 * num_objects:
                    inst_str = 'drop {}'.format(g.objects[y_out[j] - num_objects])
                elif y_out[j] < opt['y_dim'] - 1:
                    inst_str = 'go {}'.format(g.rooms[y_out[j] - 2 * num_objects])
                else:
                    inst_str = 'STOP'
                text_out[j].append(inst_str)
                if inst_str != 'STOP':
                    assert g.parse_exec(inst_str), inst_str

        return text_out


class Seq2SeqModel(nn.Module):
    def __init__(self, opt, data_agent):
        super().__init__()
        self.opt = opt

        self.input_emb = nn.Embedding(
            data_agent.wordcnt, opt['embedding_dim'], padding_idx=0
        )
        self.encoder = nn.GRU(
            opt['embedding_dim'], opt['rnn_h'], opt['rnn_layers'], batch_first=True
        )
        self.decoder = nn.GRU(
            opt['feat_dim'] + opt['y_dim'],
            opt['rnn_h'],
            opt['rnn_layers'],
            batch_first=True,
        )
        self.mapping = nn.Sequential(
            nn.Linear(opt['rnn_h'] * 2, opt['y_dim']), nn.LogSoftmax()
        )

        self.criterion = nn.CrossEntropyLoss()

    def forward(self, x, map=None, y=None, loss=True, graphs=None):
        if loss:
            return self._forward_loss(x, map, y)
        else:
            return self._forward_predict(x, graphs)

    def _forward_loss(self, x, map, y):
        """
        x: [batch, seq_in], int
        map: [batch, seq_out, feat], float
        y: [batch, seq_out, 3 * target], float, binary
        """

        opt = self.opt
        batch_size, seq_out = x.size(0), y.size(1)
        h_0 = Variable(torch.zeros(opt['rnn_layers'], batch_size, opt['rnn_h']))
        if opt['cuda']:
            h_0.cuda()

        enc_out, hidden = self.encoder(
            self.input_emb(x), h_0
        )  # [batch, seq_in, h], [layer, batch, h]
        loss = 0
        for i in range(seq_out):
            if i == 0:
                y_in = Variable(torch.zeros(batch_size, 1, y.size(2)))
                if opt['cuda']:
                    y_in.cuda()
            else:
                y_in = y[:, i - 1].unsqueeze(1)
            dec_out, hidden = self.decoder(
                torch.cat([map[:, i].unsqueeze(1), y_in], dim=2), hidden
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

    def _forward_predict(self, x, graphs):
        graphs = deepcopy(graphs)
        opt = self.opt
        batch_size = x.size(0)
        h_0 = Variable(torch.zeros(opt['rnn_layers'], batch_size, opt['rnn_h']))
        if opt['cuda']:
            h_0.cuda()

        enc_out, hidden = self.encoder(
            self.input_emb(x), h_0
        )  # [batch, seq_in, h], [layer, batch, h]
        text_out = [[] for _ in range(batch_size)]
        for i in range(opt['max_seq_out']):
            if i == 0:
                y_in = Variable(torch.zeros(batch_size, 1, opt['y_dim']))
                if opt['cuda']:
                    y_in.cuda()
            else:
                y_in = y_onehot.unsqueeze(1)
            map = Variable(torch.zeros(batch_size, 1, opt['feat_dim']))
            for j in range(batch_size):
                g = graphs[j]
                offset = 0
                for k in range(len(g.objects)):
                    if g.object2room[k] == -1:
                        map[j, 0, offset + k] = 1.0
                offset += len(g.objects)
                for k in range(len(g.objects)):
                    if g.object2room[k] == g.agent_at_room:
                        map[j, 0, offset + k] = 1.0
                offset += len(g.objects)
                map[j, 0, offset + g.agent_at_room] = 1.0
            if opt['cuda']:
                map.cuda()

            dec_out, hidden = self.decoder(torch.cat([map, y_in], dim=2), hidden)
            alpha = F.softmax(torch.bmm(enc_out, hidden[-1].unsqueeze(2)))
            attention = torch.bmm(enc_out.transpose(1, 2), alpha).squeeze(2)
            dec_out = self.mapping(
                torch.cat([attention, dec_out.squeeze(1)], dim=1)
            )  # [batch, y_dim]

            y_mask = Variable(torch.zeros(batch_size, opt['y_dim']))
            for j in range(batch_size):
                g = graphs[j]
                offset = 0
                for k in range(len(g.objects)):
                    if g.object2room[k] != g.agent_at_room:
                        y_mask[j, offset + k] = -1e7
                offset += len(g.objects)
                for k in range(len(g.objects)):
                    if g.object2room[k] != -1:
                        y_mask[j, offset + k] = -1e7
                offset += len(g.objects)
                for k in range(len(g.rooms)):
                    if k not in g.room_edges[g.agent_at_room]:
                        y_mask[j, offset + k] = -1e7
            y_mask[:, -1] = 1.0
            if opt['cuda']:
                y_mask.cuda()
            dec_out = dec_out + y_mask

            y_out = torch.max(dec_out, 1)[1].data  # [batch, 1]
            y_onehot = torch.zeros(batch_size, opt['y_dim'])  # [batch, y_dim]
            y_onehot.scatter_(1, y_out, 1)
            y_onehot = Variable(y_onehot)
            if opt['cuda']:
                y_onehot.cuda()

            y_out = y_out.squeeze()
            num_objects = opt['num_objects']
            for j in range(batch_size):
                if len(text_out[j]) > 0 and text_out[j][-1] == 'STOP':
                    continue
                g = graphs[j]
                if y_out[j] < num_objects:
                    inst_str = 'get {}'.format(g.objects[y_out[j]])
                elif y_out[j] < 2 * num_objects:
                    inst_str = 'drop {}'.format(g.objects[y_out[j] - num_objects])
                elif y_out[j] < opt['y_dim'] - 1:
                    inst_str = 'go {}'.format(g.rooms[y_out[j] - 2 * num_objects])
                else:
                    inst_str = 'STOP'
                text_out[j].append(inst_str)
                if inst_str != 'STOP':
                    assert g.parse_exec(inst_str), inst_str
        return text_out
