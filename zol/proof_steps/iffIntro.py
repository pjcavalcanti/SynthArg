from zol.expression_types.iff import Iff
from zol.expression_types.implies import Implies
from zol.proof_steps.proof import Proof


class IffIntro(Proof):
    def assumptions(self):
        return self.leftProof.assumptions() + self.rightProof.assumptions()
    def conclusion(self):
        return Iff(self.leftProof.conclusion().left, self.rightProof.conclusion().left)
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
        assert isinstance(leftProof.conclusion(), Implies)
        assert isinstance(rightProof.conclusion(), Implies)
        assert leftProof.conclusion().left == rightProof.conclusion().right
        assert leftProof.conclusion().right == rightProof.conclusion().left
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.leftProof = listOfProofs[0]
        self.rightProof = listOfProofs[1]

