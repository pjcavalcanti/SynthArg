from zol.expression_types.false import FFalse
from zol.expression_types.not_expression import Not
from zol.expression_types.truthvalue import TruthValue
from zol.proof_steps.proof import Proof


class NotElim(Proof):
    def assumptions(self):
        return self.positiveProof.assumptions() + self.negativeProof.assumptions()
    def conclusion(self):
        return FFalse()
    def descendants(self):
        return [self.positiveProof, self.negativeProof]
    
    @classmethod
    def arityProofs(cls):
        return 2
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        positiveProof = listOfProofs[0]
        negativeProof = listOfProofs[1]
        assert isinstance(positiveProof, Proof)
        assert isinstance(negativeProof, Proof)
        assert isinstance(negativeProof.conclusion(), Not)
        assert negativeProof.conclusion().descendants()[0] == positiveProof.conclusion()
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.positiveProof = listOfProofs[0]
        self.negativeProof = listOfProofs[1]

    