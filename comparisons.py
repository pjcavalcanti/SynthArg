from tqdm import tqdm
from generators import RandomExpressionZipf
from renderers import TextExpressionRenderer
from zol import Expression, Variable, And

def isFormEquivalentExpression(expr1, expr2):
    assert isinstance(expr1, Expression)
    assert isinstance(expr2, Expression)
    
    if isinstance(expr1, Variable) and isinstance(expr2, Variable):
        return True
    if not expr1.__class__ == expr2.__class__:
        return False
    
    for i in range(expr1.arity()):
        if not isFormEquivalentExpression(expr1[i], expr2[i]):
            return False
    return True

def getExpressionVariables(expr):
    assert isinstance(expr, Expression)
    
    variables = []
    def dfs(expr):
        if isinstance(expr, Variable):
            variables.append(expr)
            return
        
        for d in range(expr.descendants()):
            dfs(d)
    
    dfs(expr)
    return variables

def isIsomorphic(expr1, expr2):
    assert isinstance(expr1, Expression)
    assert isinstance(expr2, Expression)
        
    variables1 = []
    variables2 = []

    def dfs(expr1, expr2):
        if isinstance(expr1, Variable) and isinstance(expr2, Variable):
            variables1.append(expr1)
            variables2.append(expr2)
            return True
        if expr1.__class__ != expr2.__class__:
            return False
        
        descendants1 = expr1.descendants()
        descendants2 = expr2.descendants()
        for i in range(expr1.arity()):
            if not dfs(descendants1[i], descendants2[i]):
                return False
        return True
    
    if not dfs(expr1, expr2):
        return False
    
    def variablesAreIsomorphic(variables1, variables2):
        AtoB = dict()
        BtoA = dict()
        for v1, v2 in zip(variables1, variables2):
            AtoB[v1] = v2
            BtoA[v2] = v1

        for v1, v2 in zip(variables1, variables2):
            if BtoA[AtoB[v1]] != v1 or AtoB[BtoA[v2]] != v2:
                return False
        return True
    
    return variablesAreIsomorphic(variables1, variables2)

import matplotlib.pyplot as plt

exprRender = TextExpressionRenderer()
rdExprGen = RandomExpressionZipf(variables=["a, b, c, d, e, f"], maxDepth=10, a=2.1)
rdExprGen.seed(0)

expSet = set()
sizes = []
for i in tqdm(range(10000)):
    sizes.append(len(expSet))
    newExpr = rdExprGen()
    if len(expSet) > 0 and any(isIsomorphic(newExpr, e) for e in expSet):
        continue
    expSet.add(newExpr)
print(len(expSet))
plt.plot(sizes)
plt.show()

import sys

depths = []
avgExprSize = 0
for e in expSet:
    avgExprSize += sys.getsizeof(exprRender(e))
    depths.append(e.depth())
    print(sys.getsizeof(exprRender(e)))

print(avgExprSize / len(expSet))

plt.hist(depths, bins=range(1, 11), align="left", rwidth=0.8)
plt.show()