from expressions import *
from proofs import RAA, AndElimLeft, AndElimRight, AndIntro, Axiom, IffElimLeft, IffElimRight, IffIntro, ImpliesElim, ImpliesIntro, NotElim, NotIntro, AndElim, IffElim, Proof
from renderers import TextExpressionRenderer, TextProofRenderer
from generators import RandomExpressionZipf

exprrender = TextExpressionRenderer()
render = TextProofRenderer()
p = Variable("p")
q = Variable("q")
notP = Not(p)
tr = TruthValue("T")
fa = TruthValue("F")

print(exprrender(p), exprrender(q), exprrender(notP))
print(p == p, p == q, p == notP, notP == notP)
print(tr == fa, tr == tr, fa == fa, tr == p, fa == p)

ax1 = Axiom(p)
pr1 = AndIntro(ax1, ax1)
pr2 = AndElimLeft(pr1)
pr3 = AndElimRight(pr1)
pr4 = ImpliesIntro(p, pr1)
pr5 = ImpliesIntro(p, ax1)
pr6 = ImpliesElim(ax1, pr5) # from p, p -> p, infer p
pr7 = IffIntro(Axiom(Implies(And(p,p), q)), Axiom(Implies(q, And(p,p))))
pr8 = IffElimLeft(Axiom(Iff(p, q)))
pr9 = IffElimRight(Axiom(Iff(p, q)))
pr10 = NotElim(Axiom(p),Axiom(Not(p)))
pr11 = NotElim(AndIntro(Axiom(p), Axiom(p)), Axiom(Not(And(p,p))))

pr12 = NotIntro(Not(q), NotElim(Axiom(p),Axiom(Not(p))))
pr13 = NotIntro(Not(Implies(p, q)), NotElim(Axiom(Implies(p, q)),Axiom(Not(Implies(p, q)))))

# pr14 = RAA()

print(render(pr12))
print(render(pr13))
print(render(ax1))
print(render(pr1))
print(render(pr2))
print(render(pr3))
print(render(pr4))
print(render(pr5))
print(render(pr6))
print(render(pr7))
print(render(pr8))
print(render(pr9))
print(render(pr10))
print(render(pr11))





# generate a random proof!

# 1. generate a random expression
# 2. work backwards

# render = TextProofRenderer()
# exprrender = TextExpressionRenderer()

# maxDepth = 2
# a = 3
# b = 2.7
# generator = RandomExpressionZipf(["p", "q", "r"], maxDepth, a, b)
# generator.seed(20)
# expr = generator()
# print(exprrender(expr))

# expr = And(Variable("p"), Variable("q"))

# proofTypes = [AndIntro, AndElim, ImpliesIntro, ImpliesElim, IffIntro, IffElim, NotIntro, NotElim, RAA]
# proofGivenRoot = {
#     And: [Axiom, AndIntro],
#     Implies: [Axiom, ImpliesIntro],
#     Iff: [Axiom, IffIntro],
#     Not: [Axiom, NotIntro],
# }
# proofRequirements = {
#     And: [],
# }
# def proofInstructions(expr):
#     if isinstance(expr, Variable):
#         return {
#             "proofType": Axiom,
#             "proofArgs": (expr,),
#         }
#     elif isinstance(expr, Not):
#         return {
#             "proofType": NotIntro,
#             "proofArgs": (expr,),
#         }


# maxDepth = 2
# def generateRandomProof(expr):
#     proofType = proofGivenRoot[type(expr)]
#     if len(proofType) == 1:
#         return proofType[0](expr)
#     else:
#         return proofType[1](expr, generateRandomProof(expr.descendants()[0]))

# if depth < self.maxDepth:
#         shouldStop = self.randomGenerator.random() < self.probs[depth] / arity
#     else:
#         shouldStop = True

#     if shouldStop:
#         return self.randomGenerator.choice(self.leafNodes)

#     nodeType = self.randomGenerator.choice(self.unaryNodes + self.binaryNodes)
#     arity = nodeType.arity()

#     children = [self(depth + 1, arity) for _ in range(arity)]
#     expression = nodeType(*children)
#     return expression