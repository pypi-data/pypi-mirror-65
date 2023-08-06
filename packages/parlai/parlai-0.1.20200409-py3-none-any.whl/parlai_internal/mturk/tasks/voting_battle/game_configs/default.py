#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from .comment_battle import CommentBattleGC, CommentBattleRespondingOnlyGC, CommentBattleVotingOnlyGC, CommentBattleVotingOnlySoloGC
from .comment_battle_response import CommentBattleResponseGC
from .personachat import PersonachatGC, PersonachatRespondingOnlyGC, PersonachatVotingOnlyGC, PersonachatVotingOnlySoloGC
from .squad import SQuADGC, SQuADRespondingOnlyGC, SQuADVotingOnlyGC, SQuADVotingOnlySoloGC
from .vqa import VqaGC, VqaRespondingOnlyGC


class DefaultGameConfig(VqaGC):
    def __init__(self):
        super().__init__()
