from .proof import Proof
from ..expression_types.expression import Expression
from ..expression_types.or_expression import Or

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
    def validate_representation(self, listOfExpressions, listOfProofs):
        propositionAtRight = listOfExpressions[0]
        proofOfLeft = listOfProofs[0]
        assert isinstance(proofOfLeft, Proof)
        assert isinstance(propositionAtRight, Expression)
        return True
    
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.propositionAtRight = listOfExpressions[0]
        self.proofOfLeft = listOfProofs[0]
