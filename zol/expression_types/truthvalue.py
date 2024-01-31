from .expression import Expression

class TruthValue(Expression):
    _truth_values = ["T", "F"]

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
