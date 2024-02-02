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

introDict = {
    And: AndIntro,
    Or: OrIntro,
    Not: NotIntro,
    Iff: IffIntro,
    Implies: ImpliesIntro,
}
elimDict = {
    And: AndElim,
    Or: OrElim,
    Implies: ImpliesElim,
    Iff: IffElim,
    Not: NotElim,
}

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
        options = [
            ImpliesIntro(
                [expr.descendants()[0]],
                [getProofFor(expr.descendants()[1], p, currDepth + 1)],
            ),
        ]
        return random.choice(options)
    elif proofType == AndIntro:
        # To prove expr = A&B, we need to prove A and B separately,
        # i.e. we need:
        # AndIntro([], [proof(A), proof(B)])
        options = [
            AndIntro(
                [],
                [
                    getProofFor(expr.descendants()[0], p, currDepth + 1),
                    getProofFor(expr.descendants()[1], p, currDepth + 1)
                ]
            ),
        ]
        return random.choice(options)
    elif proofType == OrIntro:
        # To prove expr = A||B, we need to prove one of them
        # i.e. we need:
        # OrIntro([B], [proof(A)])
        options = [
            OrIntro(
                [expr.descendants()[1]],
                [getProofFor(expr.descendants()[0], p, currDepth + 1)]),
        ]
        return random.choice(options)
    elif proofType == IffIntro:
        # To prove expr = A<->B, we need to prove A->B and B->A
        # i.e. we need:
        # IffIntro([], [proof(A->B), proof(B->A)])
        options = [
            IffIntro(
                [],
                [
                    getProofFor(Implies(expr.descendants()[0], expr.descendants()[1]), p, currDepth + 1),
                    getProofFor(Implies(expr.descendants()[1], expr.descendants()[0]), p, currDepth + 1)
                ]),
        ]
        return random.choice(options)
    elif proofType == NotIntro:
        # To prove expr = ¬A, we need to prove ⊥ and discard A from the assumptions
        # i.e. we need:
        # NotIntro([A], [proof(FFalse)])
        options = [
            NotIntro(
                [expr.descendants()[0]],
                [getProofFor(FFalse(), p, currDepth + 1)]
            ),
        ]
        return random.choice(options)
    elif proofType == AndElim:
        # To prove expr = A with AndElim we prove A from a proof of A and B
        # i.e. we need:
        # AndElim([], [proof(A&B)])
        # 
        # We have the option of
            # B = random new expression
            # B = one of the assumptions already made
        options = [
            AndElim(
                [],
                [getProofFor(And(expr, randExpressionGen()), p, currDepth + 1)],
            ),
        ]
        if len(previousAssumptions) > 0:
            options.append(
                AndElim(
                    [],
                    [getProofFor(And(expr, random.choice(previousAssumptions)), p, currDepth + 1)],
                )
            )
        return random.choice(options)
    elif proofType == OrElim:
        # To prove C with OrElim we use a proof of A||B and two proofs of C, and eliminate A from the assumptions of the first proof(C) and B from the assumptions of the second proof(C)
        # i.e. we need:
        # OrElim([], [proof(A||B), proof(C), proof(C)])
        #
        # Note: We can use ImpliesIntro in any proof of C to get a proof of A->C and B->C,
        # so this is equivalent to eliminating A,B from A->C & B->C using A||B, therefore proving C.
        options = [
            OrElim(
                [],
                [
                    getProofFor(Or(randExpressionGen(), randExpressionGen()), p, currDepth + 1),
                    getProofFor(expr, p, currDepth + 1),
                    getProofFor(expr, p, currDepth + 1),
                ],
            ),
        ]
        return random.choice(options)
    elif proofType == ImpliesElim:
        # To prove expr = C with ImpliesElim we use a proof of A->C and a proof of A
        # i.e. we need:
        # ImpliesElim([], [proof(A), proof(A->C)])
        rndExpr = randExpressionGen()
        options = [
            ImpliesElim(
                [],
                [
                    getProofFor(rndExpr, p, currDepth + 1),
                    getProofFor(Implies(rndExpr, expr), p, currDepth + 1),
                ],
            ),
        ]
        return random.choice(options)
    elif proofType == IffElim:
        # To prove expr = A->B with IffElim we use a proof of A<->B
        # i.e. we need:
        # IffElim([], [proof(A<->B)])
        options = [
            IffElim(
                [],
                [
                    getProofFor(Iff(expr.descendants()[0], expr.descendants()[1]), p, currDepth + 1),
                ],
            ),
        ]
        return random.choice(options)
    elif proofType == NotElim:
        # To prove expr = ⊥ with NotElim we use a proof of A and a proof of ¬A
        # i.e. we need:
        # NotElim([], [proof(A), proof(¬A)])
            # Here, A can be a random expression
        rndExpr = randExpressionGen()
        options = [
            NotElim(
                [],
                [
                    getProofFor(rndExpr, p, currDepth + 1),
                    getProofFor(Not(rndExpr), p, currDepth + 1),
                ]
            )
        ]
        return random.choice(options)
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
        return random.choice(options)
    raise AssertionError(f"Proof type {str(proofType)} not implemented: \n for {str(expr)}")


random.seed(5)

rdExprGen = RandomExpressionZipf(a = 6)

exprRender = TextExpressionRenderer()
render = TextProofRenderer()


for i in range(10):
    toProve = rdExprGen()
    print(f"{i + 1}-TH PROOF :: STARTING FROM {exprRender(toProve)}")
    print(render(getProofFor(toProve, p = 0.9)))
    if i < 9:
        print()