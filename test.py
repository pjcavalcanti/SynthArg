from expressions import *
# from proofs import Proof
from renderers import TextExpressionRenderer, TextProofRenderer
from generators import RandomExpressionZipf

class Proof(TreeNode):
    def assumptions(self):
        raise NotImplementedError
    def conclusion(self):
        raise NotImplementedError
    def descendants(self):
        return NotImplementedError
    @classmethod
    def arity(cls):
        return NotImplementedError
    def __init__(self, listOfExpressions, listOfProofs):
        raise NotImplementedError
