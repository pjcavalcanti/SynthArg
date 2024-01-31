from zol.expression_types.iff import Iff
from zol.expression_types.implies import Implies
from zol.proof_steps.proof import Proof


class IffElim(Proof):
    # The same as IffElimLeft
    def assumptions(self):
        return self.iffProof.assumptions()
    def conclusion(self):
        return Implies(self.iffProof.conclusion().left, self.iffProof.conclusion().right)
    def descendants(self):
        return [self.iffProof]
    
    @classmethod
    def arityProofs(cls):
        return 1
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        iffProof = listOfProofs[0]
        assert isinstance(iffProof, Proof)
        assert isinstance(iffProof.conclusion(), Iff)
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.iffProof = listOfProofs[0]
