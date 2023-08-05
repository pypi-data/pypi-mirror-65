class Statement(object):
    def __init__(self, parent):
        self.parent = parent


class DeclarationStatement(Statement):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name


class PrintStatement(Statement):
    def __init__(self, parent, args):
        super().__init__(parent)
        self.args = args


class PromptStatement:
    def __init__(self, parent, cast_type, text):
        self.parent = parent
        self.cast_type = cast_type
        self.text = text


class AssignmentStatement(Statement):
    def __init__(self, parent, target, value):
        super().__init__(parent)
        self.target = target
        self.value = value


class Module(object):
    def __init__(self, statements):
        self.statements = statements
