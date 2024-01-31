class TreeNode():
    def descendants(self):
        raise NotImplementedError
    @classmethod
    def arity(cls):
        raise NotImplementedError
    def depth(self):
        return 1 + max([d.depth() for d in self.descendants()], default=-1)
    
class Expression(TreeNode):
    def type(self):
        raise NotImplementedError
    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.descendants() == other.descendants() 
        
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

class TruthValue(Expression):
    _truth_values = ["T", "F"]

    def type(self):
        return "TruthValue"
    def descendants(self):
        return []
    @classmethod
    def arity(cls):
        return 0
    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.name == other.name

    def __init__(self, value):
        assert value in TruthValue._truth_values
        self.name = value

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

class And(Expression):
    def type(self):
        return "And"
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
    
class Or(Expression):
    def type(self):
        return "Or"
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

class Implies(Expression):
    def type(self):
        return "Implies"
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

class Iff(Expression):
    def type(self):
        return "Iff"
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