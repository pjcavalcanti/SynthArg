from .proof import Proof
from ..expression_types.expression import Expression
from ..expression_types.not_expression import Not
from ..expression_types.truthvalue import TruthValue

class RAA(Proof):
    # UNTESTED
    def assumptions(self):
        return [a for a in self.proofOfAbsurd.assumptions() if a != Not(self.propositionToProve)]
    def conclusion(self):
        return self.propositionToProve
    def descendants(self):
        return [self.proofOfAbsurd]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, propositionToProve, proofOfAbsurd):
        assert isinstance(proofOfAbsurd, Proof)
        assert isinstance(proofOfAbsurd.conclusion(), TruthValue)
        assert proofOfAbsurd.conclusion().name == "F"
        assert isinstance(propositionToProve, Expression)
        self.proofOfAbsurd = proofOfAbsurd
        self.propositionToProve = propositionToProve
