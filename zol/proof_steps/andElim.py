from .proof import Proof
from ..expression_types.and_expression import And

class AndElim(Proof):
    def assumptions(self):
        return self.andProof.assumptions()
    def conclusion(self):
        return self.andProof.conclusion().left
    def descendants(self):
        return [self.andProof]
    
    @classmethod
    def arityProofs(cls):
        return 1
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        andProof = listOfProofs[0]
        assert isinstance(andProof, Proof)
        assert isinstance(andProof.conclusion(), And)
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.andProof = listOfProofs[0]
