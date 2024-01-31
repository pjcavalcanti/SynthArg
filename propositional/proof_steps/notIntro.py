from .proof import Proof
from ..expression_types.not_expression import Not
from ..expression_types.truthvalue import TruthValue

class NotIntro(Proof):
    def assumptions(self):
        return [a for a in self.proofOfAbsurd.assumptions() if a != self.propositionToProve.descendants()[0]]
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
        assert isinstance(propositionToProve, Not)
        self.proofOfAbsurd = proofOfAbsurd
        self.propositionToProve = propositionToProve
