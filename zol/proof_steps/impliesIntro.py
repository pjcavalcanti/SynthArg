from zol.expression_types.expression import Expression
from zol.expression_types.implies import Implies
from zol.proof_steps.proof import Proof


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
    def repr_expression_types(cls):
        return [Expression]
    @classmethod
    def repr_proof_types(cls):
        return [Proof]
    @classmethod
    def repr_proof_conclusion_types(cls):
        return [Expression]
    @classmethod
    def repr_proof_conclusion_invariants(cls, self):
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.conditionExpression = listOfExpressions[0]
        self.conclusionProof = listOfProofs[0]
