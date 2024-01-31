from zol import Variable, Not, And, Or, Implies, Iff, TruthValue
from zol import RAA, AndIntro, Axiom, IffIntro, ImpliesElim, ImpliesIntro, NotElim, NotIntro, AndElim, IffElim, Proof

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

ax1 = Axiom([p], [])
pr1 = AndIntro([], [ax1, ax1])
pr2 = AndElim([], [pr1])
pr4 = ImpliesIntro([p], [pr1])
pr5 = ImpliesIntro([p], [ax1])
pr6 = ImpliesElim([], [ax1, pr5]) # from p, p -> p, infer p
pr7 = IffIntro([], [Axiom([Implies(And(p,p), q)], []), Axiom([Implies(q, And(p,p))], [])])
pr8 = IffElim([], [Axiom([Iff(p, q)], [])])
pr10 = NotElim([], [Axiom([p], []),Axiom([Not(p)], [])])
pr11 = NotElim([], [AndIntro([], [Axiom([p], []), Axiom([p], [])]), Axiom([Not(And(p,p))], [])])

pr12 = NotIntro([Not(q)], [NotElim([], [Axiom([p], []), Axiom([Not(p)], [])])])
pr13 = NotIntro([Not(Implies(p, q))],
                [NotElim([], [Axiom([Implies(p, q)], []),
                         Axiom([Not(Implies(p, q))], [])]
                         )])

# pr14 = RAA()

print(render(pr12))
print(render(pr13))
print(render(ax1))
print(render(pr1))
print(render(pr2))
print(render(pr4))
print(render(pr5))
print(render(pr6))
print(render(pr7))
print(render(pr8))
print(render(pr10))
print(render(pr11))


