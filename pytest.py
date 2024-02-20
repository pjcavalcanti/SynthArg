from SynthExpr import Var, And, Or, Not, Implies, Iff
from SynthExpr import ToString
from SynthExpr import RandomGeneratorZipf

from generators import RandomExpressionZipf as RandomGeneratorZipfZol


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


a = 1.1
b = 2.7
maxDepth = 25
variables = [Var("p"), Var("q"), Var("r")]

rdGen = RandomGeneratorZipf(variables, maxDepth, a, b)
rdGenZol = RandomGeneratorZipfZol(variables, maxDepth, a, b)


def compareGenerationSpeeds():
    import time
    from tqdm import tqdm
    import matplotlib.pyplot as plt

    N = 1000
    batch_size = 1000
    SynthTimes = []
    ZolTimes = []

    for i in tqdm(range(N)):
        start = time.perf_counter_ns()
        for j in range(batch_size):
            rdGen()
        end = time.perf_counter_ns()
        SynthTimes.append((end - start) / (batch_size))

        start = time.perf_counter_ns()
        for j in range(batch_size):
            rdGenZol()
        end = time.perf_counter_ns()
        ZolTimes.append((end - start) / (batch_size))

    avgSynth = sum(SynthTimes) / len(SynthTimes)
    avgZol = sum(ZolTimes) / len(ZolTimes)
    stdSynth = (sum([(x - avgSynth) ** 2 for x in SynthTimes]) / len(SynthTimes)) ** 0.5
    stdZol = (sum([(x - avgZol) ** 2 for x in ZolTimes]) / len(ZolTimes)) ** 0.5

    print(f"Synth: {avgSynth} +/- {stdSynth}, error: {stdSynth / avgSynth}")
    print(f"Zol: {avgZol} +/- {stdZol}, error: {stdZol / avgZol}")

    plt.loglog()

    plt.hist(SynthTimes, bins=100, alpha=0.5, label="Synth")
    plt.hist(ZolTimes, bins=100, alpha=0.5, label="Zol")

    plt.legend(loc="upper right")
    plt.show()


compareGenerationSpeeds()
