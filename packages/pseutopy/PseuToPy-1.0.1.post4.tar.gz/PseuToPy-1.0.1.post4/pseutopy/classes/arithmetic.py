class AddSubExpression(object):
    def __init__(self, parent, terms, operators):
        self.parent = parent
        self.terms = terms
        self.operators = operators


class MultDivExpression(object):
    def __init__(self, parent, factors, operators):
        self.parent = parent
        self.factors = factors
        self.operators = operators


class PowExpression(object):
    def __init__(self, parent, sign, base, operators, exponents):
        self.parent = parent
        self.sign = sign
        self.base = base
        self.operators = operators
        self.exponents = exponents


class BaseValue(object):
    def __init__(self, parent, operand):
        self.parent = parent
        self.operand = operand


class ExponentValue(object):
    def __init__(self, parent, sign, operand):
        self.parent = parent
        self.sign = sign
        self.operand = operand



