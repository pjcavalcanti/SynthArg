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
    def arityProofs(cls):
        return 2
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        leftProof = listOfProofs[0]
        rightProof = listOfProofs[1]
        assert isinstance(leftProof, Proof)
        assert isinstance(rightProof, Proof)
        return True
    
    def __init__(self,listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.leftProof = listOfProofs[0]
        self.rightProof = listOfProofs[1]
