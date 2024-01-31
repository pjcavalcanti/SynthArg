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
    def arityProofs(cls):
        return 1
    @classmethod
    def arityExpressions(cls):
        return 1
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        conditionExpression = listOfExpressions[0]
        conclusionProof = listOfProofs[0]
        assert isinstance(conditionExpression, Expression)
        assert isinstance(conclusionProof, Proof)
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.conditionExpression = listOfExpressions[0]
        self.conclusionProof = listOfProofs[0]
