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
        assert len(listOfExpressions) == self.arityExpressions(), f"\n\tlistOfExpressions is length {len(listOfExpressions)}, but should be {self.arityExpressions()}"
        assert len(listOfProofs) == self.arityProofs(), f"\n\tlistOfProofs is length {len(listOfProofs)}, but should be {self.arityProofs()}"
        assert len(listOfProofs) == len(self.repr_proof_types()), f"\n\tlistOfProofs is length {len(listOfProofs)}, but self.repr_proof_types() is length {len(self.repr_proof_types())}"

        for expression, typeExpressionShouldBe in zip(listOfExpressions, self.repr_expression_types()):
            assert isinstance(expression, typeExpressionShouldBe), f"\n\texpression is type {type(expression)}, but should be {typeExpressionShouldBe}"
        for proof, typeProofShouldBe, typeConclusionShouldBe in zip(listOfProofs,
                                       self.repr_proof_types(),
                                       self.repr_proof_conclusion_types()):
            assert isinstance(proof, typeProofShouldBe), f"\n\tproof is type {type(proof)}, but should be {typeProofShouldBe}"
            assert isinstance(proof.conclusion(), typeConclusionShouldBe), f"\n\tproof.conclusion() is type {type(proof.conclusion())}, but should be {typeConclusionShouldBe}"
            
        # Representation values
        assert self.repr_proof_conclusion_invariants(listOfProofs)
    