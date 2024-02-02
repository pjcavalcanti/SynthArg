from zol.expression_types.expression import Expression

class Variable(Expression):
    def descendants(self):
        return []
    @classmethod
    def arity(cls):
        return 0
    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.name == other.name
    def __str__(self):
        return f"Variable({self.name})"
    def __hash__(self):
        return hash(str(self))
    
    _existing_variables = set()
    
    def __init__(self, *args):
        name = args[0]
        Variable._existing_variables.add(name)
        self.name = name