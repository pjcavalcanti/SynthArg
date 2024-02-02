from zol.expression_types.truthvalue import TruthValue

class TTrue(TruthValue):
    def __init__(self):
        super().__init__("T")