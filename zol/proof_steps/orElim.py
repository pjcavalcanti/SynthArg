from zol.expression_types.expression import Expression
from zol.expression_types.or_expression import Or
from zol.proof_steps.proof import Proof


class OrElim(Proof):
    # UNTESTED
    def assumptions(self):
        return  [a for a in self.leftProofOfP.assumptions()
                if a != self.proofOfOr.conclusion().descendants()[0]]\
                + \
                [a for a in self.rightProofOfP.assumptions()
                if a != self.proofOfOr.conclusion().descendants()[1]]
    def conclusion(self):
        return self.leftProofOfP.conclusion()
    def descendants(self):
        return [self.proofOfOr, self.leftProofOfP, self.rightProofOfP]
    
    @classmethod
    def arityProofs(cls):
        return 3
    @classmethod
    def arityExpressions(cls):
        return 0
    @classmethod
    def repr_expression_types(cls):
        return []
    @classmethod
    def repr_proof_types(cls):
        return [Proof, Proof, Proof]
    @classmethod
    def repr_proof_conclusion_types(cls):
        return [Or, Expression, Expression]
    @classmethod
    def repr_proof_conclusion_invariants(cls, listOfProofs):
        leftProofOfP = listOfProofs[1]
        rightProofOfP = listOfProofs[2]
        return leftProofOfP.conclusion() == rightProofOfP.conclusion()
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.proofOfOr = listOfProofs[0]
        self.leftProofOfP = listOfProofs[1]
        self.rightProofOfP = listOfProofs[2]
