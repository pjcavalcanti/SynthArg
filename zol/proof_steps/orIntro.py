from .proof import Proof
from ..expression_types.expression import Expression
from ..expression_types.or_expression import Or

class OrIntro(Proof):
    # UNTESTED
    # Maybe left and right versions are necessary?
    def assumptions(self):
        return self.proofOfLeft.assumptions()
    def conclusion(self):
        return Or(self.proofOfLeft.conclusion(), self.propositionAtRight)
    def descendants(self):
        return [self.proofOfLeft]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, propositionAtRight, proofOfLeft):
        assert isinstance(proofOfLeft, Proof)
        assert isinstance(propositionAtRight, Expression)
        self.proofOfLeft = proofOfLeft
        self.propositionAtRight = propositionAtRight
