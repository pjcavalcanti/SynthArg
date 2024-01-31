from .expression import Expression

class Not(Expression):
    def type(cls):
        return "Not"
    def descendants(self):
        return [self.child]
    @classmethod
    def arity(cls):
        return 1
    
    def __init__(self, child):
        assert isinstance(child, Expression)
        self.child = child
