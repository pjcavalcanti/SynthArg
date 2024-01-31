from .proof import Proof
from ..expression_types.iff import Iff
from ..expression_types.implies import Implies

class IffElim(Proof):
    # The same as IffElimLeft
    def assumptions(self):
        return self.iffProof.assumptions()
    def conclusion(self):
        return Implies(self.iffProof.conclusion().left, self.iffProof.conclusion().right)
    def descendants(self):
        return [self.iffProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, iffProof):
        assert isinstance(iffProof, Proof)
        assert isinstance(iffProof.conclusion(), Iff)
        self.iffProof = iffProof
