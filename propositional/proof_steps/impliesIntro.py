from .proof import Proof
from ..expression_types.expression import Expression
from ..expression_types.implies import Implies

class ImpliesIntro(Proof):
    def assumptions(self):
        return [a for a in self.conclusionProof.assumptions() if a != self.conditionExpression]
    def conclusion(self):
        return Implies(self.conditionExpression, self.conclusionProof.conclusion())
    def descendants(self):
        return [self.conclusionProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, conditionExpression, conclusionProof):
        assert isinstance(conditionExpression, Expression)
        assert isinstance(conclusionProof, Proof)
        self.conclusionProof = conclusionProof
        self.conditionExpression = conditionExpression
