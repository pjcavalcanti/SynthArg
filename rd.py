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

def getProofFor(expr, p = 0.1, currDepth = 0):
    randExpressionGen = RandomExpressionZipf()
    proofTypeOptions = typeOfLastStep(expr)
    
    proofType = random.choice(proofTypeOptions)
    if random.random() < p and not currDepth < 1:
        proofType = Axiom
    
    if proofType == Axiom:
        return Axiom([expr], [])
    elif proofType == ImpliesIntro:
        # TODO: Add more options,
        # at least via "condition from a random choice from current assumptions list"
        # and via "condition as a random expression"
        rndrExp = randExpressionGen()
        options = [
            ImpliesIntro(
                [expr.descendants()[0]],
                [getProofFor(expr.descendants()[1], p, currDepth + 1)],
            ),
        ]
        return random.choice(options)
    elif proofType == AndIntro:
        # TODO: Check if more options can be added
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
        # TODO: Check if more options can be added
        options = [
            OrIntro(
                [expr.descendants()[1]],
                [getProofFor(expr.descendants()[0], p, currDepth + 1)]),
        ]
        return random.choice(options)
    elif proofType == IffIntro:
        # TODO: Check if more options can be added
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
        # TODO: Check if more options can be added
        options = [
            NotIntro(
                [expr.descendants()[0]],
                [getProofFor(FFalse(), p, currDepth + 1)]
            ),
        ]
        return random.choice(options)
    elif proofType == AndElim:
        # TODO: Add more options,
        # at least via "and with a random choice from current assumptions list"
        options = [
            AndElim(
                [],
                [getProofFor(And(expr, randExpressionGen()), p, currDepth + 1)],
            ),
        ]
        return random.choice(options)
    elif proofType == OrElim:
        # TODO: Add more options,
        # at least via "or with a random choice from current assumptions list"
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
        # TODO: Add more options,
        # at least via "implies with condition from a random choice from current assumptions list"
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
        # TODO: Add more options, if possible
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
        # TODO: Add more options,
        # at least via "not rndExpr from a random choice from current assumptions list"
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
        # TODO: Add more options, if possible
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