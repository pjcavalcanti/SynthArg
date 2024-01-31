from .proof import Proof
from ..expression_types.not_expression import Not
from ..expression_types.truthvalue import TruthValue

class NotElim(Proof):
    def assumptions(self):
        return self.positiveProof.assumptions() + self.negativeProof.assumptions()
    def conclusion(self):
        return TruthValue("F")
    def descendants(self):
        return [self.positiveProof, self.negativeProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, positiveProof, negativeProof):
        assert isinstance(positiveProof, Proof)
        assert isinstance(negativeProof, Proof)
        assert isinstance(negativeProof.conclusion(), Not)
        assert negativeProof.conclusion().descendants()[0] == positiveProof.conclusion()
        self.positiveProof = positiveProof
        self.negativeProof = negativeProof