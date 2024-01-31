from zol.expression_types.and_expression import And
from zol.proof_steps.proof import Proof


class AndElim(Proof):
    def assumptions(self):
        return self.andProof.assumptions()
    def conclusion(self):
        return self.andProof.conclusion().left
    def descendants(self):
        return [self.andProof]
    
    @classmethod
    def arityProofs(cls):
        return 1
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def repr_expression_types(cls):
        return [And]
    @classmethod
    def repr_proof_types(cls):
        return [Proof]
    @classmethod
    def repr_proof_conclusion_types(cls):
        return [And]
    @classmethod
    def repr_proof_conclusion_invariants(cls, self):
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
 
        self.andProof = listOfProofs[0]

