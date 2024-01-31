from zol.expression_types.expression import Expression
from zol.expression_types.implies import Implies
from zol.proof_steps.proof import Proof


class ImpliesElim(Proof):
    def assumptions(self):
        return self.conditionProof.assumptions() + self.conclusionProof.assumptions()
    def conclusion(self):
        return self.conclusionProof.conclusion().right
    def descendants(self):
        return [self.conditionProof, self.conclusionProof]
    
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
        return [Expression, Implies]
    @classmethod
    def repr_proof_conclusion_invariants(cls, listOfProofs):
        conditionProof = listOfProofs[0]
        conclusionProof = listOfProofs[1]
        return conclusionProof.conclusion().left == conditionProof.conclusion()
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)

        self.conditionProof = listOfProofs[0]
        self.conclusionProof = listOfProofs[1]
        
