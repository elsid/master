#coding: utf-8

from uml_matcher.errors import (MultLowerTypeError, MultUpperTypeError,
    NegativeMultLower, NegativeMultUpper, MultRangeError)

def repr_multiplicity(lower, upper):
    if lower:
        if upper:
            return '[%d..%d]' % (lower, upper)
        else:
            return '[%d..*]' % lower
    else:
        if upper:
            return '[%d]' % upper
        else:
            return ''

def assert_mult_type(value, Error):
    if value is not None and not isinstance(value, int):
        raise Error(value)

def assert_mult_value(value, Error):
    if value is not None and value < 0:
        raise Error(value)

class Type(object):
    def __init__(self, classifier,
            mult_lower=1,
            mult_upper=1,
            is_ordered=False,
            is_unique=True):
        assert_mult_type(mult_lower, MultLowerTypeError)
        assert_mult_value(mult_lower, NegativeMultLower)
        assert_mult_type(mult_upper, MultUpperTypeError)
        assert_mult_value(mult_upper, NegativeMultUpper)
        if (mult_lower is not None and mult_upper is not None
                and mult_lower > mult_upper):
            raise MultRangeError(mult_lower, mult_upper)
        self.classifier = classifier
        self.mult_lower = mult_lower
        self.mult_upper = mult_upper
        self.is_ordered = is_ordered
        self.is_unique = is_unique

    def sub_equivalent_pattern(self, pattern):
        if pattern is None:
            return True
        return (self.classifier.equivalent_pattern(pattern.classifier)
            and self.equivalent_pattern_mult_range(pattern)
            and self.is_ordered == pattern.is_ordered
            and self.is_unique == pattern.is_unique)

    def equivalent_pattern_mult_range(self, pattern):
        return ((pattern.mult_lower is None
                or (self.mult_lower is not None
                    and self.mult_lower >= pattern.mult_lower))
            and (pattern.mult_upper is None
                or (self.mult_upper is not None
                    and self.mult_upper <= pattern.mult_upper)))

    def __eq__(self, other):
        if other is None  or not isinstance(other, type(self)):
            return False
        return (self.classifier == other.classifier
            and self.mult_lower == other.mult_lower
            and self.mult_upper == other.mult_upper
            and self.is_ordered == other.is_ordered
            and self.is_unique == other.is_unique)

    def __repr__(self):
        return '{classifier}{multiplicity}'.format(
            classifier=repr(self.classifier),
            multiplicity=repr_multiplicity(self.mult_lower, self.mult_upper))
