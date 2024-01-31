from abc import ABC, abstractmethod

from zol import Expression, TruthValue, Variable, Not, And, Or, Implies, Iff
from zol import Proof
from zol.proof_steps.andElim import AndElim
from zol.proof_steps.andIntro import AndIntro
from zol.proof_steps.axiom import Axiom
from zol.proof_steps.iffElim import IffElim
from zol.proof_steps.iffIntro import IffIntro
from zol.proof_steps.impliesElim import ImpliesElim
from zol.proof_steps.impliesIntro import ImpliesIntro
from zol.proof_steps.notElim import NotElim
from zol.proof_steps.notIntro import NotIntro
from zol.proof_steps.orElim import OrElim
from zol.proof_steps.orIntro import OrIntro
from zol.proof_steps.raa import RAA

class Renderer(ABC):
    @abstractmethod
    def render(self, expression):
        pass

class TextExpressionRenderer(Renderer):

    _class_aliases = {
        Axiom: "Axiom",
        AndIntro: "∧ Intro",
        AndElim: "∧ Elim",
        OrIntro: "∨ Intro",
        OrElim: "∨ Elim",
        ImpliesIntro: "→ Intro",
        ImpliesElim: "→ Elim",
        NotIntro: "¬ Intro",
        NotElim: "¬ Elim",
        RAA: "RAA",
        IffIntro: "↔ Intro",
        IffElim: "↔ Elim",
    }

    def __call__(self, expression):
        return self.render(expression)
    def render(self, expression):
        if not isinstance(expression, Expression):
            raise TypeError("expression must be an Expression")
            
        if isinstance(expression, TruthValue):
            if expression.name == "T":
                return "⊤"
            return "⊥"
        elif isinstance(expression, Variable):
            return expression.name
        elif isinstance(expression, Not):
            return f"¬{self.render(expression.child)}"
        elif isinstance(expression, And):
            return f"({self.render(expression.left)} ∧ {self.render(expression.right)})"
        elif isinstance(expression, Or):
            return f"({self.render(expression.left)} ∨ {self.render(expression.right)})"
        elif isinstance(expression, Implies):
            return f"({self.render(expression.left)} → {self.render(expression.right)})"
        elif isinstance(expression, Iff):
            return f"({self.render(expression.left)} ↔ {self.render(expression.right)})"
        else:
            arity = expression.arity()
            output = f"{self._class_aliases[type(expression)]}("
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
    _class_aliases = {
        Axiom: "Axiom",
        AndIntro: "∧ Intro",
        AndElim: "∧ Elim",
        OrIntro: "∨ Intro",
        OrElim: "∨ Elim",
        ImpliesIntro: "→ Intro",
        ImpliesElim: "→ Elim",
        NotIntro: "¬ Intro",
        NotElim: "¬ Elim",
        RAA: "RAA",
        IffIntro: "↔ Intro",
        IffElim: "↔ Elim",
    }

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
            f"{i + 1}) {self._class_aliases[type(p)]}\n" + self.indentHelper(self.assumptionsAndConclusions(p))
             for i, p in enumerate(proof.descendants())
            )
        if basedOn != "":
            basedOn = "Based on:\n" + self.indentHelper(basedOn)
        return f"{self._class_aliases[type(proof)]}" + "\n" + self.indentHelper(assAndCon + "\n" + basedOn)
        
    
    def assumptionsAndConclusions(self, proof):
        seen = set()
        assumptions = "\n".join(self.exprRend(a) for a in proof.assumptions() if self.exprRend(a) not in seen and not seen.add(self.exprRend(a)))
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
        print(f"{i + 1}) " + renderer(expression) + "\n")