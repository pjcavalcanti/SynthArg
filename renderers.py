from expressions import Expression
from abc import ABC, abstractmethod

from proofs import Proof

class Renderer(ABC):
    @abstractmethod
    def render(self, expression):
        pass

class TextExpressionRenderer(Renderer):
    def __call__(self, expression):
        return self.render(expression)
    def render(self, expression):
        if not isinstance(expression, Expression):
            raise TypeError("expression must be an Expression")
            
        if expression.type() == "TruthValue":
            if expression.name == "T":
                return "⊤"
            return "⊥"
        elif expression.type() == "Variable":
            return expression.name
        elif expression.type() == "Not":
            return f"¬{self.render(expression.child)}"
        elif expression.type() == "And":
            return f"({self.render(expression.left)} ∧ {self.render(expression.right)})"
        elif expression.type() == "Or":
            return f"({self.render(expression.left)} ∨ {self.render(expression.right)})"
        elif expression.type() == "Implies":
            return f"({self.render(expression.left)} → {self.render(expression.right)})"
        elif expression.type() == "Iff":
            return f"({self.render(expression.left)} ↔ {self.render(expression.right)})"
        else:
            arity = expression.arity()
            output = f"{expression.type()}("
            for i in range(arity):
                output += self.render(expression.descendants()[i])
                if i < arity - 1:
                    output += ", "
            if arity == 0:
                output += ")"
            else:
                output = output[:-2] + ")"
            return output
        
class TextProofRenderer(Renderer):
    def __init__(self, expressionRenderer = TextExpressionRenderer(), indent = "  "):
        self.exprRend = expressionRenderer
        self.indent = indent
    def __call__(self, proof):
        if not isinstance(proof, Proof):
            raise TypeError("proof must be a Proof")
        return self.render(proof)
    
    def render(self, proof):
        assAndCon = self.assumptionsAndConclusions(proof)
        basedOn = "\n".join(
            f"{i + 1}) {type(p)}\n" + self.indentHelper(self.assumptionsAndConclusions(p))
             for i, p in enumerate(proof.descendants())
            )
        if basedOn != "":
            basedOn = "Based on:\n" + self.indentHelper(basedOn)
        return f"{type(proof)}" + "\n" + self.indentHelper(assAndCon + "\n" + basedOn)
        
    
    def assumptionsAndConclusions(self, proof):
        assumptions = "\n".join(self.exprRend(a) for a in proof.assumptions())
        conclusion = self.exprRend(proof.conclusion())

        assumptions = f"Assumptions:\n{self.indentHelper(assumptions, 1)}"
        conclusion = f"Conclusion:\n{self.indentHelper(conclusion)}"
        return assumptions + "\n" + conclusion

    def indentHelper(self, string, times = 1):
        return self.indent * times + string.replace("\n", "\n" + self.indent * times)

if __name__ == "__main__":
    # Sample usage

    from generators import RandomExpressionZipf

    a = 3
    b = 2.7
    maxDepth = 100
    statDepths = []
    seed = 10
    
    renderer = TextExpressionRenderer()
    exprGen = RandomExpressionZipf(["p", "q", "r"], maxDepth, a, b)
    exprGen.seed(seed)
    
    print("Rendering a few random expressions:\n")
    for i in range(10):
        expression = exprGen()
        print(f"{i + 1}) - " + renderer(expression) + "\n")