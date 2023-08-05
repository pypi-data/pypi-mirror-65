class Num(object):
    def __init__(self, parent, n):
        self.parent = parent
        self.n = n


class Name(object):
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id


class Boolean(object):
    def __init__(self, parent, boolean_value):
        self.parent = parent
        self.boolean_value = boolean_value


class Range:
    def __init__(self, parent, start, stop, step):
        self.parent = parent
        self.start = start
        self.stop = stop
        self.step = step
