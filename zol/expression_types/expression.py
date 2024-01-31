class Expression():
    def descendants(self):
        raise NotImplementedError
    @classmethod
    def arity(cls):
        raise NotImplementedError
    
    def depth(self):
        return 1 + max([d.depth() for d in self.descendants()], default=-1)
    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.descendants() == other.descendants() 
    def __init__(self, *args):
        raise NotImplementedError