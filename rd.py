import random
from renderers import TextExpressionRenderer, TextProofRenderer
from zol import Expression, Variable, Implies, And, Or, Not, Iff
from zol import AndIntro, AndElim, ImpliesElim, ImpliesIntro, RAA, OrIntro, OrElim, RAA
from zol.expression_types.false import FFalse
from zol.proof_steps.axiom import Axiom
from zol.proof_steps.iffElim import IffElim
from zol.proof_steps.iffIntro import IffIntro
from zol.proof_steps.notElim import NotElim
from zol.proof_steps.notIntro import NotIntro
from zol.proof_steps.raa import RAA

from generators import RandomExpressionZipf

def typeOfLastStep(expr):
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

def getProofFor(expr, p = 0.1, currDepth = 0, previousAssumptions = []):
    randExpressionGen = RandomExpressionZipf()
    proofTypeOptions = typeOfLastStep(expr)
    
    proofType = random.choice(proofTypeOptions)
    if random.random() < p and not currDepth < 1:
        proofType = Axiom
    
    if proofType == Axiom:

        return Axiom([expr], [])
    
    elif proofType == ImpliesIntro:
        # To prove expr = A->B, we need to prove B and discard A from the assumptions
        # i.e. we need:
        # Implies([A], [proof(B)])

        A = expr.descendants()[0]
        B = expr.descendants()[1]
        proofB = getProofFor(B, p, currDepth + 1)
        
        return ImpliesIntro([A], [proofB])
    
    elif proofType == AndIntro:
        # To prove expr = A&B, we need to prove A and B separately,
        # i.e. we need:
        # AndIntro([], [proof(A), proof(B)])

        A = expr.descendants()[0]
        B = expr.descendants()[1]
        proofA = getProofFor(A, p, currDepth + 1)
        proofB = getProofFor(B, p, currDepth + 1)

        return AndIntro([], [proofA, proofB])
    
    elif proofType == OrIntro:
        # To prove expr = A||B, we need to prove one of them
        # i.e. we need:
        # OrIntro([B], [proof(A)])

        A = expr.descendants()[0]
        B = expr.descendants()[1]
        proofA = getProofFor(A, p, currDepth + 1)

        return OrIntro([B], [proofA])
    
    elif proofType == IffIntro:
        # To prove expr = A<->B, we need to prove A->B and B->A
        # i.e. we need:
        # IffIntro([], [proof(A->B), proof(B->A)])

        A = expr.descendants()[0]
        B = expr.descendants()[1]
        proofAiB = getProofFor(Implies(A, B), p, currDepth + 1)
        proofBiA = getProofFor(Implies(B, A), p, currDepth + 1)
        
        return IffIntro([], [proofAiB, proofBiA])
    
    elif proofType == NotIntro:
        # To prove expr = ¬A, we need to prove ⊥ and discard A from the assumptions
        # i.e. we need:
        # NotIntro([A], [proof(FFalse)])
    
        A = expr.descendants()[0]
        proofFalse = getProofFor(FFalse(), p, currDepth + 1)

        return NotIntro([A], [proofFalse])
    
    elif proofType == AndElim:
        # To prove expr = A with AndElim we prove A from a proof of A and B
        # i.e. we need:
        # AndElim([], [proof(A&B)])
        # 
        # We have the option of
            # B = random new expression

        A = expr
        B = randExpressionGen()

        return AndElim([], [getProofFor(And(A, B), p, currDepth + 1)])
    
    elif proofType == OrElim:
        # To prove C with OrElim we use a proof of A||B and two proofs of C, and eliminate A from the assumptions of the first proof(C) and B from the assumptions of the second proof(C)
        # i.e. we need:
        # OrElim([], [proof(A||B), proof(C), proof(C)])
        #
        # Note: We can use ImpliesIntro in any proof of C to get a proof of A->C and B->C,
        # so this is equivalent to eliminating A,B from A->C & B->C using A||B, therefore proving C.

        C = expr
        A = randExpressionGen()
        B = randExpressionGen()
        proofAorB = getProofFor(Or(A, B), p, currDepth + 1)
        proofC1 = getProofFor(C, p, currDepth + 1)
        proofC2 = getProofFor(C, p, currDepth + 1)

        return OrElim([], [proofAorB, proofC1, proofC2])
        
    elif proofType == ImpliesElim:
        # To prove expr = C with ImpliesElim we use a proof of A->C and a proof of A
        # i.e. we need:
        # ImpliesElim([], [proof(A), proof(A->C)])
        
        C = expr
        A = randExpressionGen()
        proofA = getProofFor(A, p, currDepth + 1)
        proofAiC = getProofFor(Implies(A, C), p, currDepth + 1)

        return ImpliesElim([], [proofA, proofAiC])
        
    elif proofType == IffElim:
        # To prove expr = A->B with IffElim we use a proof of A<->B
        # i.e. we need:
        # IffElim([], [proof(A<->B)])
        
        A = expr.descendants()[0]
        B = expr.descendants()[1]
        proofAiffB = getProofFor(Iff(A, B), p, currDepth + 1)
    
        return IffElim([], [proofAiffB])
    
    elif proofType == NotElim:
        # To prove expr = ⊥ with NotElim we use a proof of A and a proof of ¬A
        # i.e. we need:
        # NotElim([], [proof(A), proof(¬A)])
            # Here, A can be a random expression

        A = randExpressionGen()
        proofA = getProofFor(A, p, currDepth + 1)
        proofNotA = getProofFor(Not(A), p, currDepth + 1)

        return NotElim([], [proofA, proofNotA])

    elif proofType == RAA:
        # To prove expr = A with RAA we use a proof of ⊥ and discard ¬A from the assumptions
        # i.e. we need:
        # RAA([A], [proof(FFalse)])

        options = [
            RAA(
                [expr],
                [getProofFor(FFalse(), p, currDepth + 1)],
            )
        ]
        A = expr
        proofFalse = getProofFor(FFalse(), p, currDepth + 1)

        return RAA([A], [proofFalse])
    
    raise AssertionError(f"Proof type {str(proofType)} not implemented: \n for {str(expr)}")


random.seed(5)

rdExprGen = RandomExpressionZipf(a = 3)

exprRender = TextExpressionRenderer()
render = TextProofRenderer()


for i in range(10000):
    toProve = rdExprGen()
    print(f"{i + 1}-TH PROOF :: STARTING FROM {exprRender(toProve)}")
    print(render(getProofFor(toProve, p = 0.4)))
    if i < 9:
        print()