# coding: utf-8


class MultLowerTypeError(Exception):
    def __init__(self, value):
        super(MultLowerTypeError, self).__init__(
            'type of multiplicity lower is not int: %s' % type(value))


class MultUpperTypeError(Exception):
    def __init__(self, value):
        super(MultUpperTypeError, self).__init__(
            'type of multiplicity upper is not int: %s' % type(value))


class NegativeMultLower(Exception):
    def __init__(self, value):
        super(NegativeMultLower, self).__init__(
            'multiplicity lower bound is negative: %d' % value)


class NegativeMultUpper(Exception):
    def __init__(self, value):
        super(NegativeMultUpper, self).__init__(
            'multiplicity upper bound is negative: %d' % value)


class MultRangeError(Exception):
    def __init__(self, lower, upper):
        super(MultRangeError, self).__init__(
            'multiplicity range error: lower(%d) > upper(%d)' % (lower, upper))


class CheckVariantFailed(Exception):
    def __init__(self, variant, equivalent, connection):
        self.variant = variant
        self.equivalent = equivalent
        self.connection = connection

    def __str__(self):

        def generate():
            for e in self.variant.equivalents:
                base = '%s === %s' % (e.target, e.pattern)
                color = self.connection.color
                end_type = self.connection.end_type
                if e == self.equivalent:
                    yield '  %s <<< %s (%s)' % (base, color, end_type)
                else:
                    yield '  ' + base

        return 'check variant failed\n%s' % '\n'.join(generate())

    def __repr__(self):
        return 'CheckVariantFailed(%s, %s, %s)' % tuple(repr(x) for x in (
            self.variant, self.equivalent, self.connection))
