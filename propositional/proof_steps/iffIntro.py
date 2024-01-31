from .proof import Proof
from ..expression_types.iff import Iff

class IffIntro(Proof):
    def assumptions(self):
        return self.leftProof.assumptions() + self.rightProof.assumptions()
    def conclusion(self):
        return Iff(self.leftProof.conclusion().left, self.rightProof.conclusion().left)
    def descendants(self):
        return [self.leftProof, self.rightProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, leftProof, rightProof):
        assert isinstance(leftProof, Proof)
        assert isinstance(rightProof, Proof)
        assert leftProof.conclusion().type() == "Implies"
        assert rightProof.conclusion().type() == "Implies"
        assert leftProof.conclusion().left == rightProof.conclusion().right
        assert leftProof.conclusion().right == rightProof.conclusion().left

        self.leftProof = leftProof
        self.rightProof = rightProof
