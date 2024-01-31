from zol.expression_types.expression import Expression
from zol.expression_types.false import FFalse
from zol.expression_types.not_expression import Not
from zol.expression_types.truthvalue import TruthValue
from zol.proof_steps.proof import Proof


class NotElim(Proof):
    def assumptions(self):
        return self.positiveProof.assumptions() + self.negativeProof.assumptions()
    def conclusion(self):
        return FFalse()
    def descendants(self):
        return [self.positiveProof, self.negativeProof]
    
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
        return [Expression, Not]
    @classmethod
    def repr_proof_conclusion_invariants(cls, listOfProofs):
        if not listOfProofs[1].conclusion() == Not(listOfProofs[0].conclusion()):
            return False
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):    
        super().__init__(listOfExpressions, listOfProofs)

        self.positiveProof = listOfProofs[0]
        self.negativeProof = listOfProofs[1]

    