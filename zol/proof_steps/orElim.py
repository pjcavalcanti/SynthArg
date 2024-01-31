from .proof import Proof
from ..expression_types.or_expression import Or

class OrElim(Proof):
    # UNTESTED
    def assumptions(self):
        return  [a for a in self.leftProofOfP.assumptions()
                if a != self.proofOfOr.conclusion().descendants()[0]]\
                + \
                [a for a in self.rightProofOfP.assumptions()
                if a != self.proofOfOr.conclusion().descendants()[1]]
    def conclusion(self):
        return self.leftProofOfP.conclusion()
    def descendants(self):
        return [self.proofOfOr, self.leftProofOfP, self.rightProofOfP]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, proofOfOr, leftProofOfP, rightProofOfP):
        assert isinstance(proofOfOr, Proof)
        assert isinstance(proofOfOr, Or)
        assert isinstance(leftProofOfP, Proof)
        assert isinstance(rightProofOfP, Proof)
        assert leftProofOfP.conclusion() == rightProofOfP.conclusion()
        self.proofOfOr = proofOfOr
        self.leftProofOfP = leftProofOfP
        self.rightProofOfP = rightProofOfP
