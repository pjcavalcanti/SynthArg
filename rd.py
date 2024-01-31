from zol import Implies, Variable, Proof, ImpliesIntro
from zol.expression_types.expression import Expression

p = Variable("p")
q = Variable("q")

toProve = Implies(p, q)

# def expressionArgumentsRequirements(expr):
#     elif isinstance(expr, Variable):
#         nArguments = ImpliesIntro.arityProofs()
#         argumentTypes = [Proof]
#     if isinstance(expr, Implies):
#         nArguments = ImpliesIntro.arityExpressions()
#         argumentTypes = [Expression]
#     return {
#         "nArguments": nArguments,
#         "argumentTypes": argumentTypes,
#     }
