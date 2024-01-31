from zol.expression_types.expression import Expression
from zol.expression_types.or_expression import Or
from zol.proof_steps.proof import Proof


class OrIntro(Proof):
    # UNTESTED
    # Maybe left and right versions are necessary?
    def assumptions(self):
        return self.proofOfLeft.assumptions()
    def conclusion(self):
        return Or(self.proofOfLeft.conclusion(), self.propositionAtRight)
    def descendants(self):
        return [self.proofOfLeft]
    
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
        
        self.propositionAtRight = listOfExpressions[0]
        self.proofOfLeft = listOfProofs[0]
