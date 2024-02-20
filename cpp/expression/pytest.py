from SynthExpr import Var, And, Or, Not, Implies, Iff
from SynthExpr import ToString
from SynthExpr import RandomGeneratorZipf

from ...generators import RandomExpressionZipf as RandomGeneratorZipfZol


def testFormulas():
    p = Var("p")
    q = Var("q")
    p_and_q = And(p, q)
    p_or_q = Or(p, q)
    not_p = Not(p)
    p_implies_q = Implies(p, q)
    p_iff_q = Iff(p, q)

    toString = ToString()

    print(p)
    print(q)
    print(p_and_q)
    print(p_or_q)
    print(not_p)
    print(p_implies_q)
    print(p_iff_q)
    print(toString(p))
    print(toString(q))
    print(toString(p_and_q))
    print(toString(p_or_q))
    print(toString(not_p))
    print(toString(p_implies_q))
    print(toString(p_iff_q))


rdGen = RandomGeneratorZipf()
rdGenZol = RandomGeneratorZipfZol()
rdGen.seed(1)
for _ in range(10):
    print(rdGenZol())
    # print(toString(rdGen()))
