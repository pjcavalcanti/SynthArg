from zol.expression_types.expression import Expression
from zol.expression_types.false import FFalse
from zol.expression_types.not_expression import Not
from zol.expression_types.truthvalue import TruthValue
from zol.proof_steps.proof import Proof


class RAA(Proof):
    # UNTESTED
    def assumptions(self):
        return [a for a in self.proofOfAbsurd.assumptions() if a !=Not(self.propositionToProve)]
    def conclusion(self):
        return self.propositionToProve
    def descendants(self):
        return [self.proofOfAbsurd]
    
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
        return [FFalse]
    @classmethod
    def repr_proof_conclusion_invariants(cls, self):
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.propositionToProve = listOfExpressions[0]
        self.proofOfAbsurd = listOfProofs[0]
