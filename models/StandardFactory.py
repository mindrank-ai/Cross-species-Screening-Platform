import os
import sys
from .ImportTools import *

from .Utils import logit, timeit, checkit
from .M2VEmbedding import M2VEmbedding
from .M2VScoring import M2VScoring
from .D3Embedding import D3Embedding
from .D3Scoring import D3Scoring
from .StrucEmbedding import StrucEmbedding
from .StrucScoring import StrucScoring


class StandardFactory():
    @staticmethod
    def get_factory(factory):
        if factory == 'embedding':
            return EmbeddingFactory()
        elif factory == 'scoring':
            return ScoringFactory()
        raise TypeError('Unknown Factory.')
        
class EmbeddingFactory():
    def get_instance(self, method):
        try:
            return getattr(self, f"_get_{method}")()
        except Exception as e:
            print(e)
            return -1 
        
    def _get_m2v(self):
        return M2VEmbedding
    def _get_d3(self):
        return D3Embedding
    def _get_struc(self):
        return StrucEmbedding

class ScoringFactory():
    def get_instance(self, method):
        try:
            return getattr(self, f"_get_{method}")()
        except Exception as e:
            print(e)
            return -1 
        
    def _get_m2v(self):
        return M2VScoring
    def _get_d3(self):
        return D3Scoring
    def _get_struc(self):
        return StrucScoring