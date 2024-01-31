from zol.expression_types.and_expression import And
from zol.expression_types.expression import Expression
from zol.proof_steps.proof import Proof


class AndIntro(Proof):
    def assumptions(self):
        return self.leftProof.assumptions() + self.rightProof.assumptions()
    def conclusion(self):
        return And(self.leftProof.conclusion(), self.rightProof.conclusion())
    def descendants(self):
        return [self.leftProof, self.rightProof]
    
    @classmethod
    def arityProofs(cls):
        return 2
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def repr_expression_types(cls):
        return []
    @classmethod
    def repr_proof_types(cls):
        return [Proof, Proof]
    @classmethod
    def repr_proof_conclusion_types(cls):
        return [Expression, Expression]
    @classmethod
    def repr_proof_conclusion_invariants(cls, self):
        return True
    
    def __init__(self,listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.leftProof = listOfProofs[0]
        self.rightProof = listOfProofs[1]

