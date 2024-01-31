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
    def validate_representation(self, listOfExpressions, listOfProofs):
        proofOfOr = listOfProofs[0]
        leftProofOfP = listOfProofs[1]
        rightProofOfP = listOfProofs[2]
        assert isinstance(proofOfOr, Proof)
        assert isinstance(proofOfOr, Or)
        assert isinstance(leftProofOfP, Proof)
        assert isinstance(rightProofOfP, Proof)
        assert leftProofOfP.conclusion() == rightProofOfP.conclusion()
        return True
    
    def __init__(self, listOfExpressions, listOfProofs):
        super().__init__(listOfExpressions, listOfProofs)
        
        self.proofOfOr = listOfProofs[0]
        self.leftProofOfP = listOfProofs[1]
        self.rightProofOfP = listOfProofs[2]
