from pseutopy.classes.statements import Statement


class FunctionDefinitionStatement(Statement):
    def __init__(self, parent, name, args, body):
        super().__init__(parent)
        self.name = name
        self.args = args
        self.body = body


class FunctionCallStatement(Statement):
    def __init__(self, parent, name, args):
        super().__init__(parent)
        self.name = name
        self.args = args


class ReturnStatement(Statement):
    def __init__(self, parent, value):
        super().__init__(parent)
        self.value = value
