from random import Random
from zol import Iff, Implies, Not, And, Or, Variable

class RandomExpressionZipf():
    # Generates random expressions by extending a branch of the expression tree
    # with a probability that decreases with the depth of the branch.
    # The probability of extending a branch of depth Depth is:
    #
    #       1 - sum_{d <= Depth} 1 / (d + b) ** a / arity_of_currNode.
    #
    # We stop extending if we reach a maximum depth.
    def __init__(self, variables = ["p", "q", "r"], maxDepth = 0, a = 3, b = 2.7):
        self.randomGenerator = Random()

        self.varNames = variables
        self.unaryNodes = [Not]
        self.binaryNodes = [And, Or, Implies, Iff]
        self.leafNodes = [Variable(x) for x in self.varNames]

        self.maxDepth = maxDepth
        self.a = a
        self.b = b
        self.probs = [1 / (i + b) ** a for i in range(1, maxDepth + 1)]
        self.probs = [p + sum(self.probs[:i]) for i, p in enumerate(self.probs)]
        self.probs = [p / self.probs[-1] for p in self.probs]

    def seed(self, seed):
        self.randomGenerator.seed(seed)

    def __call__(self, depth = 0, arity = 1):
        if depth < self.maxDepth:
            shouldStop = self.randomGenerator.random() < self.probs[depth] / arity
        else:
            shouldStop = True

        if shouldStop:
            return self.randomGenerator.choice(self.leafNodes)

        nodeType = self.randomGenerator.choice(self.unaryNodes + self.binaryNodes)
        arity = nodeType.arity()

        children = [self(depth + 1, arity) for _ in range(arity)]
        expression = nodeType(*children)
        return expression