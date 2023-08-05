class List(object):
    def __init__(self, parent, elements, empty):
        self.parent = parent
        self.elements = elements
        self.empty = empty


class ListGetElement:
    def __init__(self, parent, index, list_expr):
        self.parent = parent
        self.index = index
        self.list_expr = list_expr


class ListAddElementStatement:
    def __init__(self, parent, element, list_expr, index):
        self.parent = parent
        self.element = element
        self.list_expr = list_expr
        self.index = index


class ListRemoveElementStatement:
    def __init__(self, parent, index, list_expr):
        self.parent = parent
        self.index = index
        self.list_expr = list_expr


class ListRemoveAndGetElementStatement:
    def __init__(self, parent, index, list_expr):
        self.parent = parent
        self.index = index
        self.list_expr = list_expr


class ListRemoveFirstElementStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListRemoveAndGetFirstElementStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListRemoveLastElementStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListRemoveAndGetLastElementStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListLengthStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListMinStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListMaxStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


class ListSumStatement:
    def __init__(self, parent, list_expr):
        self.parent = parent
        self.list_expr = list_expr


