class Expression():
    def descendants(self):
        raise NotImplementedError
    @classmethod
    def arity(cls):
        raise NotImplementedError
    
    def depth(self):
        return 1 + max([d.depth() for d in self.descendants()], default=-1)
    def __init__(self, *args):
        raise NotImplementedError
    def __str__(self):
        output = self.__class__.__name__ + "("
        for d in self.descendants():
            output += str(d) + ", "
        if self.arity() > 0:
            output = output[:-2] + ")"
        else:
            output += ")"
        return output
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.descendants() == other.descendants()
    def __hash__(self):
        return hash(str(self))
