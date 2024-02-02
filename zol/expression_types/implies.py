from zol.expression_types.expression import Expression

class Implies(Expression):
    def descendants(self):
        return [self.left, self.right]
    @classmethod
    def arity(cls):
        return 2

    def __init__(self, left, right):
        assert isinstance(left, Expression)
        assert isinstance(right, Expression)
        self.left = left
        self.right = right
