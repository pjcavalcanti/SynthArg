from .truthvalue import TruthValue

class FFalse(TruthValue):
    def __init__(self):
        super().__init__("F")