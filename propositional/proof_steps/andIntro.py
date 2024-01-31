from .proof import Proof
from ..expression_types.and_expression import And

class AndIntro(Proof):
    def assumptions(self):
        return self.leftProof.assumptions() + self.rightProof.assumptions()
    def conclusion(self):
        return And(self.leftProof.conclusion(), self.rightProof.conclusion())
    def descendants(self):
        return [self.leftProof, self.rightProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, leftProof, rightProof):
        assert isinstance(leftProof, Proof)
        assert isinstance(rightProof, Proof)
        self.leftProof = leftProof
        self.rightProof = rightProof