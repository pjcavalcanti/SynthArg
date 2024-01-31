from typing import List

from zol.expression_types.expression import Expression


class Proof():
    def assumptions(self):
        raise NotImplementedError
    def conclusion(self):
        raise NotImplementedError
    def descendants(self):
        return NotImplementedError
    
    @classmethod
    def arityProofs(cls):
        return NotImplementedError
    @classmethod
    def arityExpressions(cls):
        return NotImplementedError
    @classmethod
    def repr_expression_types(cls):
        return NotImplementedError
    @classmethod
    def repr_proof_types(cls):
        return NotImplementedError
    @classmethod
    def repr_proof_conclusion_types(cls):
        return NotImplementedError
    @classmethod
    def repr_proof_conclusion_invariants(cls, self):
        return NotImplementedError
    
    def __init__(self, listOfExpressions: List[Expression], listOfProofs: List['Proof']) -> None:
        # Guarantees representation is correct
        # Representation types
        assert len(listOfProofs) == self.arityProofs()
        assert len(listOfExpressions) == self.arityExpressions()

        for expression, typeProofShouldBe in zip(listOfExpressions, self.repr_expression_types()):
            assert isinstance(expression, typeProofShouldBe)
        for proof, typeProofShouldBe, typeConclusionShouldBe in zip(listOfProofs,
                                       self.repr_proof_types(),
                                       self.repr_proof_conclusion_types()):
            assert isinstance(proof, typeProofShouldBe)
            assert isinstance(proof.conclusion(), typeConclusionShouldBe)
            
        # Representation values
        assert self.repr_proof_conclusion_invariants(listOfProofs)
    