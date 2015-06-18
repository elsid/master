# coding: utf-8

import yaml
from utils import cached_eq
from pattern_matcher.errors import (
    MultLowerTypeError, MultUpperTypeError, NegativeMultLower,
    NegativeMultUpper, MultRangeError)
from pattern_matcher.eq_pattern import eq_pattern
from pattern_matcher.element import Element


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


class Type(Element):
    def __init__(self,
                 classifier=None,
                 lower=1,
                 upper=1,
                 is_ordered=None,
                 is_unique=None):
        super(Type, self).__init__()
        assert_mult_type(lower, MultLowerTypeError)
        assert_mult_value(lower, NegativeMultLower)
        assert_mult_type(upper, MultUpperTypeError)
        assert_mult_value(upper, NegativeMultUpper)
        if (lower is not None and upper is not None
                and lower > upper):
            raise MultRangeError(lower, upper)
        self.classifier = classifier
        self.lower = lower
        self.upper = upper
        self.is_ordered = is_ordered
        self.is_unique = is_unique

    @cached_eq
    def equiv_pattern(self, pattern):
        return (super(Type, self).equiv_pattern(pattern)
                and self.equiv_pattern_range(pattern)
                and eq_pattern(self.is_ordered, pattern.is_ordered)
                and eq_pattern(self.is_unique, pattern.is_unique))

    def equiv_pattern_range(self, pattern):
        return ((pattern.lower is None
                 or (self.lower is not None
                     and self.lower >= pattern.lower))
                and (pattern.upper is None
                     or (self.upper is not None
                         and self.upper <= pattern.upper)))

    @property
    def name(self):
        return self.classifier.name

    @property
    def full_name(self):
        return self.name

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Type)
                and self.classifier == other.classifier
                and self.lower == other.lower
                and self.upper == other.upper
                and self.is_ordered == other.is_ordered
                and self.is_unique == other.is_unique)

    def __str__(self):
        return 'type of {classifier}{multiplicity}'.format(
            classifier=str(self.classifier),
            multiplicity=repr_multiplicity(self.lower, self.upper))

    def __repr__(self):
        return 'Type(%s)' % repr(self.classifier)

    @staticmethod
    def yaml_representer(dumper, value):
        return Type._yaml_representer(
            dumper, value,
            classifier=value.classifier,
            lower=value.lower if value.lower != 1 else None,
            upper=value.upper if value.upper != 1 else None,
            is_ordered=value.is_ordered,
            is_unique=value.is_unique,
        )


yaml.add_representer(Type, Type.yaml_representer)
yaml.add_constructor('!Type', Type.yaml_constructor)
