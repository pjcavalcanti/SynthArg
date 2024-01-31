from .proof import Proof
from ..expression_types.implies import Implies

class ImpliesElim(Proof):
    def assumptions(self):
        return self.conditionProof.assumptions() + self.conclusionProof.assumptions()
    def conclusion(self):
        return self.conclusionProof.conclusion().right
    def descendants(self):
        return [self.conditionProof, self.conclusionProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, conditionProof, implicationProof):
        assert isinstance(conditionProof, Proof)
        assert isinstance(implicationProof, Proof)
        assert isinstance(implicationProof.conclusion(), Implies)
        self.conditionProof = conditionProof
        self.conclusionProof = implicationProof
