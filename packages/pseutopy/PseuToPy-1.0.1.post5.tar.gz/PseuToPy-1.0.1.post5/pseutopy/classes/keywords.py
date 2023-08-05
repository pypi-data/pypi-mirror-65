from pseutopy.classes.statements import Statement


class BreakStatement(Statement):
    def __init__(self, parent, _):
        super().__init__(parent)
        self._ = _


class ContinueStatement(Statement):
    def __init__(self, parent, _):
        super().__init__(parent)
        self._ = _


class PassStatement(Statement):
    def __init__(self, parent, _):
        super().__init__(parent)
        self._ = _
