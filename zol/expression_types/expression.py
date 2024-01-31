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