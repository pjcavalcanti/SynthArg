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
    def validate_representation(self):
        raise NotImplementedError
    
    def __init__(self, listOfExpressions: List[Expression], listOfProofs: List['Proof']) -> None:
        assert len(listOfProofs) == self.arityProofs()
        assert len(listOfExpressions) == self.arityExpressions()

        for expression in listOfExpressions:
            assert isinstance(expression, Expression)
        for proof in listOfProofs:
            assert isinstance(proof, Proof)

        isValidRep = self.validate_representation(listOfExpressions, listOfProofs)
        assert type(isValidRep) == bool
        assert isValidRep
    