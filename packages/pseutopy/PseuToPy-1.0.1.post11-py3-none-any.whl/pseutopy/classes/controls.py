from pseutopy.classes.statements import Statement


class IfStatement(Statement):
    def __init__(self, parent, test, body, orelse):
        super().__init__(parent)
        self.test = test
        self.body = body
        self.orelse = orelse


class ElseStatement(Statement):
    def __init__(self, parent, body):
        super().__init__(parent)
        self.body = body


class ElseIfStatement(Statement):
    def __init__(self, parent, test, body):
        super().__init__(parent)
        self.test = test
        self.body = body


class WhileStatement(Statement):
    def __init__(self, parent, test, body, orelse):
        super().__init__(parent)
        self.test = test
        self.body = body
        self.orelse = orelse


class ForStatement(Statement):
    def __init__(self, parent, target, iterations, body, orelse):
        super().__init__(parent)
        self.target = target
        self.iterations = iterations
        self.body = body
        self.orelse = orelse