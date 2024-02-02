
from generators import RandomExpressionZipf, RandomProofZipf
from renderers import TextExpressionRenderer, TextProofRenderer


exprRender = TextExpressionRenderer()
proofRender = TextProofRenderer()

rdExprGen = RandomExpressionZipf(a = 2, b = 3)
rdProofGen = RandomProofZipf(a = 2, b = 3, randomExpressionGenerator=rdExprGen)

for i in range(10000):
    proof = rdProofGen()
    print(f"{i + 1}-TH PROOF :: {exprRender(proof.conclusion())}")
    print(proofRender(proof))
    if i < 9:
        print()