#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.agents.transformer.transformer import TransformerGeneratorAgent
from parlai.core.torch_agent import History
from parlai_internal.agents.retnref.retnref import RetnrefAgent, RetnrefHistory


RETRIEVAL_MODEL_FILE = '/checkpoint/parlai/projects/retrieve_st/sweeps_ems/s2020_03_09__imagechat_retriever/001/fd8_jobid=18/model'
RET_FCP = ''  # We pass in no candidate file to force using the train cands of our task
STYLE_SEP_TOKEN = ' STYLE '


"""
Example usage: (train on IGC generative task, finetuning model from dodeca)

python examples/train_model.py -t internal:comment_battle:ImageDialogGeneration -m internal:retnref_style --choose-label-pct 0.1 --init-model /checkpoint/parlai/zoo/new_reddit/newreddit_trained20190909_usedfordodeca/model --dict-file /checkpoint/parlai/zoo/new_reddit/newreddit_trained20190909_usedfordodeca/model.dict --embedding-size 512 --n-layers 8 --ffn-size 2048 --dropout 0.1 --n-heads 16 --learn-positional-embeddings True --n-positions 512 --variant xlm --activation gelu --skip-generation True --fp16 True --text-truncate 512 --label-truncate 128 --dict-tokenizer bpe --dict-lower True -lr 1e-06 --optimizer adamax --lr-scheduler reduceonplateau --gradient-clip 0.1 -veps 0.25 --betas 0.9,0.999 --update-freq 1 --attention-dropout 0.0 --relu-dropout 0.0 --skip-generation True -vp 15 -stim 60 -vme 5000 -bs 16 -vmt ppl -vmm min --save-after-valid True -mf /tmp/retnrefstyle --set-retriever-gpu False
"""


class RetnrefStyleHistory(RetnrefHistory):
    """
    Modify history to save the style, in addition to the retriever's response.
    """

    def __init__(self, opt, **kwargs):
        super().__init__(opt, **kwargs)
        self.style = None

    def reset(self):
        super().reset()
        self.style = None

    def update_history(self, obs, retriever_response=None):
        super().update_history(obs, retriever_response=retriever_response)
        self.style = obs.get('personality')
        # This is dependent on IGC, will change for other tasks
        # If obs does not contain 'personality' (i.e. at the end of an epoch during
        # validation), there will be no style

    def get_history_str(self):
        history_str = super().get_history_str()
        if history_str is not None and self.style is not None:
            history_str += STYLE_SEP_TOKEN + self.style

        return history_str

    def get_history_vec(self):
        history = super().get_history_vec()

        if history is not None and self.style is not None:
            style = STYLE_SEP_TOKEN + self.style
            style_tok = self.parse(style)
            if self.vec_type == 'deque':
                history.extend(style_tok)
            else:
                history += style_tok

        return history

    def get_history_vec_no_ret(self):
        """
        Get the history response without the retriever or style.
        """
        hist = super(
            RetnrefHistory, self
        ).get_history_vec()  # call method from regular history class
        if hist is None:
            return []
        return hist


class RetnrefStyleAgent(RetnrefAgent):
    """
    General purpose retrieve and refine generator.
    """

    @classmethod
    def history_class(cls):
        """
        Determine the history class: this is useful for appending the style.
        """
        return RetnrefStyleHistory

    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent.
        """
        RetnrefAgent.add_cmdline_args(argparser)
        argparser.set_defaults(ret_model_file=RETRIEVAL_MODEL_FILE, ret_fcp=RET_FCP)
        return argparser


class StyleControlHistory(History):
    """
    Modify history to save the style, but without a retriever response.
    """

    # TODO: most of this is duplicated from RetnrefStyleHistory: fix this!

    def __init__(self, opt, **kwargs):
        super().__init__(opt, **kwargs)
        self.style = None

    def reset(self):
        super().reset()
        self.style = None

    def update_history(self, obs):
        super().update_history(obs)
        self.style = obs.get('personality')
        # This is dependent on IGC, will change for other tasks
        # If obs does not contain 'personality' (i.e. at the end of an epoch during
        # validation), there will be no style

    def get_history_str(self):
        history_str = super().get_history_str()
        if history_str is not None and self.style is not None:
            history_str += STYLE_SEP_TOKEN + self.style

        return history_str

    def get_history_vec(self):
        history = super().get_history_vec()

        if history is not None and self.style is not None:
            style = STYLE_SEP_TOKEN + self.style
            style_tok = self.parse(style)
            if self.vec_type == 'deque':
                history.extend(style_tok)
            else:
                history += style_tok

        return history


class StyleControlAgent(TransformerGeneratorAgent):
    """
    General purpose generator with a style in the history.
    """

    @classmethod
    def history_class(cls):
        """
        Determine the history class in order to append the style.
        """
        return StyleControlHistory
