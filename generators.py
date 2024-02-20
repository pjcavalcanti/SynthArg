import random
from zol import Iff, Implies, Not, And, Or, Variable
from zol.expression_types.false import FFalse
from zol.proof_steps.axiom import Axiom
from zol.proof_steps.andElim import AndElim
from zol.proof_steps.andIntro import AndIntro
from zol.proof_steps.iffElim import IffElim
from zol.proof_steps.iffIntro import IffIntro
from zol.proof_steps.impliesElim import ImpliesElim
from zol.proof_steps.impliesIntro import ImpliesIntro
from zol.proof_steps.notElim import NotElim
from zol.proof_steps.notIntro import NotIntro
from zol.proof_steps.orElim import OrElim
from zol.proof_steps.orIntro import OrIntro
from zol.proof_steps.raa import RAA
from zol.proof_steps.proof import Proof


class RandomExpressionGenerator:
    def ___init__(self, *args, **kwargs):
        raise NotImplementedError

    def seed(self, seed):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class RandomExpressionZipf(RandomExpressionGenerator):
    # Generates random expressions by extending a branch of the expression tree
    # with a probability that decreases with the depth of the branch.
    # The probability of extending a branch of depth Depth is:
    #
    #       1 - sum_{d <= Depth} 1 / (d + b) ** a / arity_of_currNode.
    #
    # We stop extending if we reach a maximum depth.
    def __init__(self, variables=["p", "q", "r"], maxDepth=5, a=3, b=2.7):
        self.randomGenerator = random.Random()

        self.varNames = variables
        self.unaryNodes = [Not]
        self.binaryNodes = [And, Or, Implies, Iff]
        self.leafNodes = [Variable(x) for x in self.varNames]

        self.maxDepth = maxDepth
        self.a = a
        self.b = b
        self.probs = [1 / (i + b) ** a for i in range(1, maxDepth + 1)]
        self.probs = [p + sum(self.probs[:i]) for i, p in enumerate(self.probs)]
        self.probs = [p / self.probs[-1] for p in self.probs]

    def seed(self, seed):
        self.randomGenerator.seed(seed)

    def __call__(self):
        return self._getRandomExpr(0, 1)

    def _getRandomExpr(self, currDepth=0, currArity=1):
        if currDepth < self.maxDepth:
            shouldStop = (
                self.randomGenerator.random() < self.probs[currDepth] / currArity
            )
        else:
            shouldStop = True

        if shouldStop:
            return self.randomGenerator.choice(self.leafNodes)

        nodeType = self.randomGenerator.choice(self.unaryNodes + self.binaryNodes)
        currArity = nodeType.arity()

        children = [
            self._getRandomExpr(currDepth + 1, currArity) for _ in range(currArity)
        ]
        expression = nodeType(*children)
        return expression


class RandomProofZipf:

    @staticmethod
    def _typeOfLastStep(expr):
        typeOfExpr = type(expr)
        possibleTypes = [Axiom, AndElim, OrElim, ImpliesElim, RAA]
        if typeOfExpr == Implies:
            possibleTypes.append(ImpliesIntro)
            possibleTypes.append(IffElim)
        elif typeOfExpr == And:
            possibleTypes.append(AndIntro)
        elif typeOfExpr == Or:
            possibleTypes.append(OrIntro)
        elif typeOfExpr == Not:
            possibleTypes.append(NotIntro)
        elif typeOfExpr == FFalse:
            possibleTypes.append(NotElim)
        elif typeOfExpr == Iff:
            possibleTypes.append(IffIntro)
        return possibleTypes

    def __init__(
        self, maxDepth=10, a=3, b=2.7, randomExpressionGenerator=RandomExpressionZipf()
    ):
        assert isinstance(randomExpressionGenerator, RandomExpressionGenerator)

        self.randExpressionGen = randomExpressionGenerator
        self.randomGenerator = random.Random()
        self.maxDepth = maxDepth
        self.a = a
        self.b = b
        self.probs = [1 / (i + b) ** a for i in range(1, maxDepth + 1)]
        self.probs = [p + sum(self.probs[:i]) for i, p in enumerate(self.probs)]
        self.probs = [p / self.probs[-1] for p in self.probs]

    def seed(self, seed):
        self.randomGenerator.seed(seed)
        self.randExpressionGen.seed(seed + 1)

    def __call__(self):
        return self._getProofFor(self.randExpressionGen())

    def _getProofFor(self, expr, currDepth=0, currArity=1):
        if currDepth < self.maxDepth:
            shouldStop = (
                self.randomGenerator.random() < self.probs[currDepth] / currArity
            )
        else:
            shouldStop = True

        if shouldStop:
            return Axiom([expr], [])

        proofTypeOptions = self._typeOfLastStep(expr)

        ## FIX STOPING MECANISM

        proofType = random.choice(proofTypeOptions)

        if proofType == Axiom:
            return Axiom([expr], [])

        elif proofType == ImpliesIntro:
            # To prove expr = A->B, we need to prove B and discard A from the assumptions
            # i.e. we need:
            # Implies([A], [proof(B)])

            A = expr.descendants()[0]
            B = expr.descendants()[1]
            proofB = self._getProofFor(B, currDepth + 1, currArity)

            return ImpliesIntro([A], [proofB])

        elif proofType == AndIntro:
            # To prove expr = A&B, we need to prove A and B separately,
            # i.e. we need:
            # AndIntro([], [proof(A), proof(B)])

            A = expr.descendants()[0]
            B = expr.descendants()[1]
            proofA = self._getProofFor(A, currDepth + 1, currArity)
            proofB = self._getProofFor(B, currDepth + 1, currArity)

            return AndIntro([], [proofA, proofB])

        elif proofType == OrIntro:
            # To prove expr = A||B, we need to prove one of them
            # i.e. we need:
            # OrIntro([B], [proof(A)])

            A = expr.descendants()[0]
            B = expr.descendants()[1]
            proofA = self._getProofFor(A, currDepth + 1, currArity)

            return OrIntro([B], [proofA])

        elif proofType == IffIntro:
            # To prove expr = A<->B, we need to prove A->B and B->A
            # i.e. we need:
            # IffIntro([], [proof(A->B), proof(B->A)])

            A = expr.descendants()[0]
            B = expr.descendants()[1]
            proofAiB = self._getProofFor(Implies(A, B), currDepth + 1, currArity)
            proofBiA = self._getProofFor(Implies(B, A), currDepth + 1, currArity)

            return IffIntro([], [proofAiB, proofBiA])

        elif proofType == NotIntro:
            # To prove expr = ¬A, we need to prove ⊥ and discard A from the assumptions
            # i.e. we need:
            # NotIntro([A], [proof(FFalse)])

            A = expr.descendants()[0]
            proofFalse = self._getProofFor(FFalse(), currDepth + 1, currArity)

            return NotIntro([A], [proofFalse])

        elif proofType == AndElim:
            # To prove expr = A with AndElim we prove A from a proof of A and B
            # i.e. we need:
            # AndElim([], [proof(A&B)])
            #
            # We have the option of
            # B = random new expression

            A = expr
            B = self.randExpressionGen()
            proofAandB = self._getProofFor(And(A, B), currDepth + 1, currArity)

            return AndElim([], [proofAandB])

        elif proofType == OrElim:
            # To prove C with OrElim we use a proof of A||B and two proofs of C, and eliminate A from the assumptions of the first proof(C) and B from the assumptions of the second proof(C)
            # i.e. we need:
            # OrElim([], [proof(A||B), proof(C), proof(C)])
            #
            # Note: We can use ImpliesIntro in any proof of C to get a proof of A->C and B->C,
            # so this is equivalent to eliminating A,B from A->C & B->C using A||B, therefore proving C.

            C = expr
            A = self.randExpressionGen()
            B = self.randExpressionGen()
            proofAorB = self._getProofFor(Or(A, B), currDepth + 1, currArity)
            proofC1 = self._getProofFor(C, currDepth + 1, currArity)
            proofC2 = self._getProofFor(C, currDepth + 1, currArity)

            return OrElim([], [proofAorB, proofC1, proofC2])

        elif proofType == ImpliesElim:
            # To prove expr = C with ImpliesElim we use a proof of A->C and a proof of A
            # i.e. we need:
            # ImpliesElim([], [proof(A), proof(A->C)])

            C = expr
            A = self.randExpressionGen()
            proofA = self._getProofFor(A, currDepth + 1, currArity)
            proofAiC = self._getProofFor(Implies(A, C), currDepth + 1, currArity)

            return ImpliesElim([], [proofA, proofAiC])

        elif proofType == IffElim:
            # To prove expr = A->B with IffElim we use a proof of A<->B
            # i.e. we need:
            # IffElim([], [proof(A<->B)])

            A = expr.descendants()[0]
            B = expr.descendants()[1]
            proofAiffB = self._getProofFor(Iff(A, B), currDepth + 1, currArity)

            return IffElim([], [proofAiffB])

        elif proofType == NotElim:
            # To prove expr = ⊥ with NotElim we use a proof of A and a proof of ¬A
            # i.e. we need:
            # NotElim([], [proof(A), proof(¬A)])
            # Here, A can be a random expression

            A = self.randExpressionGen()
            proofA = self._getProofFor(A, currDepth + 1, currArity)
            proofNotA = self._getProofFor(Not(A), currDepth + 1, currArity)

            return NotElim([], [proofA, proofNotA])

        elif proofType == RAA:
            # To prove expr = A with RAA we use a proof of ⊥ and discard ¬A from the assumptions
            # i.e. we need:
            # RAA([A], [proof(FFalse)])

            options = [
                RAA(
                    [expr],
                    [self._getProofFor(FFalse(), currDepth + 1, currArity)],
                )
            ]
            A = expr
            proofFalse = self._getProofFor(FFalse(), currDepth + 1, currArity)

            return RAA([A], [proofFalse])

        raise AssertionError(
            f"Proof type {str(proofType)} not implemented: \n for {str(expr)}"
        )
