from zol.expression_types.expression import Expression
from zol.proof_steps.proof import Proof


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
    def repr_expression_types(cls):
        return [Expression]
    @classmethod
    def repr_proof_types(cls):
        return []
    @classmethod
    def repr_proof_conclusion_types(cls):
        return []
    @classmethod
    def repr_proof_conclusion_invariants(cls, self):
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.axiomExpresion = listOfExpressions[0]
