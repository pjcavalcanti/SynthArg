from .expression import Expression
        
class Variable(Expression):
    def type(self):
        return "Variable"
    def descendants(self):
        return []
    @classmethod
    def arity(cls):
        return 0
    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.name == other.name
    
    _existing_variables = set()
    
    def __init__(self, *args):
        name = args[0]
        Variable._existing_variables.add(name)
        self.name = name