#coding: utf-8

class MultLowerTypeError(Exception):
    def __init__(self, value):
        super().__init__('type of multiplicity lower is not int: %s'
            % type(value))

class MultUpperTypeError(Exception):
    def __init__(self, value):
        super().__init__('type of multiplicity upper is not int: %s'
            % type(value))

class NegativeMultLower(Exception):
    def __init__(self, value):
        super().__init__('multiplicity lower bound is negative: %d' % value)

class NegativeMultUpper(Exception):
    def __init__(self, value):
        super().__init__('multiplicity upper bound is negative: %d' % value)

class MultRangeError(Exception):
    def __init__(self, lower, upper):
        super().__init__('multiplicity range error: lower(%d) > upper(%d)' %
            (lower, upper))
