from .proof import Proof
from ..expression_types.expression import Expression

class Axiom(Proof):
    def assumptions(self):
        return [self.axiomExpresion]
    def conclusion(self):
        return self.axiomExpresion
    def descendants(self):
        return []
    
    @classmethod
    def arityProofs(cls):
        return 0
    @classmethod
    def arityExpressions(cls):
        return 1
    @classmethod
    def validate_representation(self, listOfExpressions, listOfProofs):
        expression = listOfExpressions[0]
        assert isinstance(expression, Expression)
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.axiomExpresion = listOfExpressions[0]
