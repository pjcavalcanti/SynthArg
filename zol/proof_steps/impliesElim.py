from zol.expression_types.implies import Implies
from zol.proof_steps.proof import Proof


class ImpliesElim(Proof):
    def assumptions(self):
        return self.conditionProof.assumptions() + self.conclusionProof.assumptions()
    def conclusion(self):
        return self.conclusionProof.conclusion().right
    def descendants(self):
        return [self.conditionProof, self.conclusionProof]
    
    @classmethod
    def arityProofs(cls):
        return 2
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        conditionProof = listOfProofs[0]
        implicationProof = listOfProofs[1]
        assert isinstance(conditionProof, Proof)
        assert isinstance(implicationProof, Proof)
        assert isinstance(implicationProof.conclusion(), Implies)
        assert implicationProof.conclusion().left == conditionProof.conclusion()
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.conditionProof = listOfProofs[0]
        self.conclusionProof = listOfProofs[1]
