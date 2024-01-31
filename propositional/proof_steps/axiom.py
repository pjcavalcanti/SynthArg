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
    def arity(cls):
        return 0
    
    def __init__(self, expression):
        assert isinstance(expression, Expression)
        self.axiomExpresion = expression