#!/usr/bin/env python3
from .bi_encoder_ranker import BiEncoderRankerAgent  # NOQA
from .cross_encoder_ranker import CrossEncoderRankerAgent  # NOQA
from .cross_encoder_ranker_dup import CrossEncoderRankerDupAgent  # NOQA
from .both_encoder_ranker import BothEncoderRankerAgent  # NOQA
from .bi_encoder_multioutput import BiEncoderRankerMultiOutputAgent  # NOQA
from .polyencoder_ranker import PolyencoderRankerAgent
from parlai.core.torch_agent import TorchAgent
from parlai.core.dict import DictionaryAgent

class RedditBiEncoderRanker(BiEncoderRankerAgent):
    """ Bi-encoder ranker that initializes the model with the weights
        pretrained from Reddit instead
    """

    def __init__(self, opt, shared=None):
        opt['reddit_initialization'] = True
        super().__init__(opt, shared)
        self.START_IDX = 2
        self.END_IDX = 2

    def set_special_idx(self):
        self.NULL_IDX = 0
        self.START_IDX = 2
        self.END_IDX = 2

    @staticmethod
    def dictionary_class():
        """ Goes back to Dictionary agent (BPE for which the path is provided
            in parameters)
        """
        return DictionaryAgent



class RedditCrossEncoderRanker(CrossEncoderRankerAgent):
    """ Bi-encoder ranker that initializes the model with the weights
        pretrained from Reddit instead
    """

    def __init__(self, opt, shared=None):
        opt['reddit_initialization'] = True
        super().__init__(opt, shared)
        self.START_IDX = 2
        self.END_IDX = 2

    def set_special_idx(self):
        self.NULL_IDX = 0
        self.START_IDX = 2
        self.END_IDX = 2

    @staticmethod
    def dictionary_class():
        """ Goes back to Dictionary agent (BPE for which the path is provided
            in parameters)
        """
        return DictionaryAgent

class RedditCrossEncoderRankerDup(CrossEncoderRankerDupAgent):
    """ Bi-encoder ranker that initializes the model with the weights
        pretrained from Reddit instead
    """

    def __init__(self, opt, shared=None):
        opt['reddit_initialization'] = True
        super().__init__(opt, shared)
        self.START_IDX = 2
        self.END_IDX = 2

    def set_special_idx(self):
        self.NULL_IDX = 0
        self.START_IDX = 2
        self.END_IDX = 2

    @staticmethod
    def dictionary_class():
        """ Goes back to Dictionary agent (BPE for which the path is provided
            in parameters)
        """
        return DictionaryAgent

class RedditBiMOEncoderRanker(BiEncoderRankerMultiOutputAgent):
    """ Bi-encoder ranker that initializes the model with the weights
        pretrained from Reddit instead
    """

    def __init__(self, opt, shared=None):
        opt['reddit_initialization'] = True
        super().__init__(opt, shared)
        self.START_IDX = 2
        self.END_IDX = 2

    def set_special_idx(self):
        self.NULL_IDX = 0
        self.START_IDX = 2
        self.END_IDX = 2

    @staticmethod
    def dictionary_class():
        """ Goes back to Dictionary agent (BPE for which the path is provided
            in parameters)
        """
        return DictionaryAgent

class RedditPolyEncoderRanker(PolyencoderRankerAgent):
    """ Bi-encoder ranker that initializes the model with the weights
        pretrained from Reddit instead
    """

    def __init__(self, opt, shared=None):
        opt['reddit_initialization'] = True
        super().__init__(opt, shared)
        self.START_IDX = 2
        self.END_IDX = 2

    def set_special_idx(self):
        self.NULL_IDX = 0
        self.START_IDX = 2
        self.END_IDX = 2

    @staticmethod
    def dictionary_class():
        """ Goes back to Dictionary agent (BPE for which the path is provided
            in parameters)
        """
        return DictionaryAgent
