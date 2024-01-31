from .proof import Proof
from ..expression_types.and_expression import And

class AndElim(Proof):
    # The same as AndElimRight
    def assumptions(self):
        return self.andProof.assumptions()
    def conclusion(self):
        return self.andProof.conclusion().left
    def descendants(self):
        return [self.andProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, andProof):
        assert isinstance(andProof, Proof)
        assert isinstance(andProof.conclusion(), And)
        self.andProof = andProof