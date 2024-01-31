from expressions import Expression, Iff, Implies, Or, TreeNode, And, TruthValue, Not

class Proof(TreeNode):
    def type(self):
        raise NotImplementedError
    def assumptions(self):
        raise NotImplementedError
    def conclusion(self):
        raise NotImplementedError

class Axiom(Proof):
    def type(self):
        return "Axiom"
    def assumptions(self):
        return [self.axiomExpresion]
    def conclusion(self):
        return self.axiomExpresion
    def descendants(self):
        return []
    @classmethod
    def arity(cls):
        return 0
    
    def __init__(self, expression):
        assert isinstance(expression, Expression)
        self.axiomExpresion = expression

class AndIntro(Proof):
    def type(self):
        return "AndIntro"
    def assumptions(self):
        return self.leftProof.assumptions() + self.rightProof.assumptions()
    def conclusion(self):
        return And(self.leftProof.conclusion(), self.rightProof.conclusion())
    def descendants(self):
        return [self.leftProof, self.rightProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, leftProof, rightProof):
        assert isinstance(leftProof, Proof)
        assert isinstance(rightProof, Proof)
        self.leftProof = leftProof
        self.rightProof = rightProof

class AndElim(Proof):
    # The same as AndElimRight
    def type(self):
        return "AndElim"
    def assumptions(self):
        return self.andProof.assumptions()
    def conclusion(self):
        return self.andProof.conclusion().left
    def descendants(self):
        return [self.andProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, andProof):
        assert isinstance(andProof, Proof)
        assert isinstance(andProof.conclusion(), And)
        self.andProof = andProof

class AndElimRight(Proof):
    def type(self):
        return "AndElimRight"
    def assumptions(self):
        return self.andProof.assumptions()
    def conclusion(self):
        return self.andProof.conclusion().left
    def descendants(self):
        return [self.andProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, andProof):
        assert isinstance(andProof, Proof)
        assert isinstance(andProof.conclusion(), And)
        self.andProof = andProof

class AndElimLeft(Proof):
    def type(self):
        return "AndElimLeft"
    def assumptions(self):
        return self.andProof.assumptions()
    def conclusion(self):
        return self.andProof.conclusion().right
    def descendants(self):
        return [self.andProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, andProof):
        assert isinstance(andProof, Proof)
        assert isinstance(andProof.conclusion(), And)
        self.andProof = andProof

class ImpliesIntro(Proof):
    def type(self):
        return "ImpliesIntro"
    def assumptions(self):
        return [a for a in self.conclusionProof.assumptions() if a != self.conditionExpression]
    def conclusion(self):
        return Implies(self.conditionExpression, self.conclusionProof.conclusion())
    def descendants(self):
        return [self.conclusionProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, conditionExpression, conclusionProof):
        assert isinstance(conditionExpression, Expression)
        assert isinstance(conclusionProof, Proof)
        self.conclusionProof = conclusionProof
        self.conditionExpression = conditionExpression

class ImpliesElim(Proof):
    def type(self):
        return "ImpliesElim"
    def assumptions(self):
        return self.conditionProof.assumptions() + self.conclusionProof.assumptions()
    def conclusion(self):
        return self.conclusionProof.conclusion().right
    def descendants(self):
        return [self.conditionProof, self.conclusionProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, conditionProof, implicationProof):
        assert isinstance(conditionProof, Proof)
        assert isinstance(implicationProof, Proof)
        assert isinstance(implicationProof.conclusion(), Implies)
        self.conditionProof = conditionProof
        self.conclusionProof = implicationProof

class IffIntro(Proof):
    def type(self):
        return "IffIntro"
    def assumptions(self):
        return self.leftProof.assumptions() + self.rightProof.assumptions()
    def conclusion(self):
        return Iff(self.leftProof.conclusion().left, self.rightProof.conclusion().left)
    def descendants(self):
        return [self.leftProof, self.rightProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, leftProof, rightProof):
        assert isinstance(leftProof, Proof)
        assert isinstance(rightProof, Proof)
        assert leftProof.conclusion().type() == "Implies"
        assert rightProof.conclusion().type() == "Implies"
        assert leftProof.conclusion().left == rightProof.conclusion().right
        assert leftProof.conclusion().right == rightProof.conclusion().left

        self.leftProof = leftProof
        self.rightProof = rightProof

class IffElim(Proof):
    # The same as IffElimLeft
    def type(self):
        return "IffElim"
    def assumptions(self):
        return self.iffProof.assumptions()
    def conclusion(self):
        return Implies(self.iffProof.conclusion().left, self.iffProof.conclusion().right)
    def descendants(self):
        return [self.iffProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, iffProof):
        assert isinstance(iffProof, Proof)
        assert isinstance(iffProof.conclusion(), Iff)
        self.iffProof = iffProof

class IffElimLeft(Proof):
    def type(self):
        return "IffElimLeft"
    def assumptions(self):
        return self.iffProof.assumptions()
    def conclusion(self):
        return Implies(self.iffProof.conclusion().left, self.iffProof.conclusion().right)
    def descendants(self):
        return [self.iffProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, iffProof):
        assert isinstance(iffProof, Proof)
        assert isinstance(iffProof.conclusion(), Iff)
        self.iffProof = iffProof

class IffElimRight(Proof):
    def type(self):
        return "IffElimRight"
    def assumptions(self):
        return self.iffProof.assumptions()
    def conclusion(self):
        return Implies(self.iffProof.conclusion().right, self.iffProof.conclusion().left)
    def descendants(self):
        return [self.iffProof]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, iffProof):
        assert isinstance(iffProof, Proof)
        assert isinstance(iffProof.conclusion(), Iff)
        self.iffProof = iffProof

class NotElim(Proof):
    def type(self):
        return "NotElim"
    def assumptions(self):
        return self.positiveProof.assumptions() + self.negativeProof.assumptions()
    def conclusion(self):
        return TruthValue("F")
    def descendants(self):
        return [self.positiveProof, self.negativeProof]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, positiveProof, negativeProof):
        assert isinstance(positiveProof, Proof)
        assert isinstance(negativeProof, Proof)
        assert isinstance(negativeProof.conclusion(), Not)
        assert negativeProof.conclusion().descendants()[0] == positiveProof.conclusion()
        self.positiveProof = positiveProof
        self.negativeProof = negativeProof

class NotIntro(Proof):
    def type(self):
        return "NotIntro"
    def assumptions(self):
        return [a for a in self.proofOfAbsurd.assumptions() if a != self.propositionToProve.descendants()[0]]
    def conclusion(self):
        return self.propositionToProve
    def descendants(self):
        return [self.proofOfAbsurd]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, propositionToProve, proofOfAbsurd):
        assert isinstance(proofOfAbsurd, Proof)
        assert isinstance(proofOfAbsurd.conclusion(), TruthValue)
        assert proofOfAbsurd.conclusion().name == "F"
        assert isinstance(propositionToProve, Not)
        self.proofOfAbsurd = proofOfAbsurd
        self.propositionToProve = propositionToProve

class RAA(Proof):
    # UNTESTED
    def type(self):
        return "RAA"
    def assumptions(self):
        return [a for a in self.proofOfAbsurd.assumptions() if a != Not(self.propositionToProve)]
    def conclusion(self):
        return self.propositionToProve
    def descendants(self):
        return [self.proofOfAbsurd]
    
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, propositionToProve, proofOfAbsurd):
        assert isinstance(proofOfAbsurd, Proof)
        assert isinstance(proofOfAbsurd.conclusion(), TruthValue)
        assert proofOfAbsurd.conclusion().name == "F"
        assert isinstance(propositionToProve, Expression)
        self.proofOfAbsurd = proofOfAbsurd
        self.propositionToProve = propositionToProve

class OrIntro(Proof):
    # UNTESTED
    # Maybe left and right versions are necessary?
    def type(self):
        return "OrIntro"
    def assumptions(self):
        return self.proofOfLeft.assumptions()
    def conclusion(self):
        return Or(self.proofOfLeft.conclusion(), self.propositionAtRight)
    def descendants(self):
        return [self.proofOfLeft]
    
    @classmethod
    def arity(cls):
        return 2
    
    def __init__(self, propositionAtRight, proofOfLeft):
        assert isinstance(proofOfLeft, Proof)
        assert isinstance(propositionAtRight, Expression)
        self.proofOfLeft = proofOfLeft
        self.propositionAtRight = propositionAtRight

class OrElim(Proof):
    # UNTESTED
    def type(self):
        return "OrElim"
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
    def arity(cls):
        return 2
    
    def __init__(self, proofOfOr, leftProofOfP, rightProofOfP):
        assert isinstance(proofOfOr, Proof)
        assert isinstance(proofOfOr, Or)
        assert isinstance(leftProofOfP, Proof)
        assert isinstance(rightProofOfP, Proof)
        assert leftProofOfP.conclusion() == rightProofOfP.conclusion()
        self.proofOfOr = proofOfOr
        self.leftProofOfP = leftProofOfP
        self.rightProofOfP = rightProofOfP

# print(a.assumptions())
# print(a.conclusion())
# print(b.assumptions())
# print(b.conclusion())