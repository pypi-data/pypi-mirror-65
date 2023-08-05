class Expression(object):
    def __init__(self, parent, logical_terms, operators):
        self.parent = parent
        self.logical_terms = logical_terms
        self.operators = operators


class AndExpression(object):
    def __init__(self, parent, logical_factors, operators):
        self.parent = parent
        self.logical_factors = logical_factors
        self.operators = operators


class BooleanTerm(object):
    def __init__(self, parent, sign, operand):
        self.parent = parent
        self.sign = sign
        self.operand = operand


class ComparisonExpression(object):
    def __init__(self, parent, left, operator, right):
        self.parent = parent
        self.left = left
        self.operator = operator
        self.right = right



