# coding: utf-8

from graph_matcher import cached_eq
from uml_matcher.errors import (
    MultLowerTypeError, MultUpperTypeError, NegativeMultLower,
    NegativeMultUpper, MultRangeError)
from uml_matcher.eq_pattern import eq_pattern, equiv_pattern


def repr_multiplicity(lower, upper):
    if lower:
        if upper:
            return ('' if lower == 1 and upper == 1
                    else '[%d..%d]' % (lower, upper))
        else:
            return '[%d..*]' % lower
    else:
        if upper:
            return '[%d]' % upper
        else:
            return ''


def assert_mult_type(value, make_error):
    if value is not None and not isinstance(value, int):
        raise make_error(value)


def assert_mult_value(value, make_error):
    if value is not None and value < 0:
        raise make_error(value)


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

    @cached_eq
    def sub_equiv_pattern(self, pattern):
        return (isinstance(pattern, Type)
                and equiv_pattern(self.classifier, pattern.classifier)
                and self.equiv_pattern_mult_range(pattern)
                and eq_pattern(self.is_ordered, pattern.is_ordered)
                and eq_pattern(self.is_unique, pattern.is_unique))

    def equiv_pattern_mult_range(self, pattern):
        return ((pattern.mult_lower is None
                 or (self.mult_lower is not None
                     and self.mult_lower >= pattern.mult_lower))
                and (pattern.mult_upper is None
                     or (self.mult_upper is not None
                         and self.mult_upper <= pattern.mult_upper)))

    @property
    def name(self):
        return self.classifier.name

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Type)
                and self.classifier == other.classifier
                and self.mult_lower == other.mult_lower
                and self.mult_upper == other.mult_upper
                and self.is_ordered == other.is_ordered
                and self.is_unique == other.is_unique)

    def __str__(self):
        return 'type of {classifier}{multiplicity}'.format(
            classifier=str(self.classifier),
            multiplicity=repr_multiplicity(self.mult_lower, self.mult_upper))

    def __repr__(self):
        return 'Type(%s)' % repr(self.classifier)
