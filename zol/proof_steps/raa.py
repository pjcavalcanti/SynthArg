from zol.expression_types.expression import Expression
from zol.expression_types.not_expression import Not
from zol.expression_types.truthvalue import TruthValue
from zol.proof_steps.proof import Proof


class RAA(Proof):
    # UNTESTED
    def assumptions(self):
        return [a for a in self.proofOfAbsurd.assumptions() if a != Not(self.propositionToProve)]
    def conclusion(self):
        return self.propositionToProve
    def descendants(self):
        return [self.proofOfAbsurd]
    
    @classmethod
    def arityProofs(cls):
        return 1
    @classmethod
    def arityExpressions(cls):
        return 1
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        propositionToProve = listOfExpressions[0]
        proofOfAbsurd = listOfProofs[0]
        assert isinstance(proofOfAbsurd, Proof)
        assert isinstance(proofOfAbsurd.conclusion(), TruthValue)
        assert proofOfAbsurd.conclusion().name == "F"
        assert isinstance(propositionToProve, Expression)
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.propositionToProve = listOfExpressions[0]
        self.proofOfAbsurd = listOfProofs[0]
