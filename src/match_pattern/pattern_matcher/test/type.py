# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, calling, raises, equal_to, starts_with
from pattern_matcher.type import Type, repr_multiplicity
from pattern_matcher.errors import (
    MultLowerTypeError, MultUpperTypeError, NegativeMultLower,
    NegativeMultUpper, MultRangeError)
Class = __import__('pattern_matcher.class', fromlist=['Class']).Class


class ReprMultiplicity(TestCase):
    def test_different_combinations_should_succeed(self):
        assert_that(repr_multiplicity(None, None), equal_to(''))
        assert_that(repr_multiplicity(42, None), equal_to('[42..*]'))
        assert_that(repr_multiplicity(None, 42), equal_to('[42]'))
        assert_that(repr_multiplicity(13, 42), equal_to('[13..42]'))
        assert_that(repr_multiplicity(1, 1), equal_to(''))


class MakeType(TestCase):
    def test_sub_equivalent_pattern_should_succeed(self):
        assert_that(Type(Class()).equiv_pattern(Type(Class())))

    def test_equivalent_pattern_range_should_succeed(self):
        assert_that(Type(Class()).equiv_pattern_range(Type(Class())))

    def test_eq_should_succeed(self):
        assert_that(Type(Class()), not equal_to(Type(Class())))
        assert_that(Type(Class('A')), equal_to(Type(Class('A'))))

    def test_str_should_succeed(self):
        assert_that(str(Type(Class())),
                    starts_with('type of class anonymous_'))
        assert_that(str(Type(Class('A'))), equal_to('type of class A'))

    def test_make_with_wrong_lower_should_throw_exception(self):
        assert_that(calling(lambda: Type(lower='')),
                    raises(MultLowerTypeError))
        assert_that(calling(lambda: Type(lower=-1)),
                    raises(NegativeMultLower))

    def test_make_with_wrong_upper_should_throw_exception(self):
        assert_that(calling(lambda: Type(upper='')),
                    raises(MultUpperTypeError))
        assert_that(calling(lambda: Type(upper=-1)),
                    raises(NegativeMultUpper))

    def test_make_with_wrong_range_should_throw_exception(self):
        assert_that(calling(lambda: Type(lower=1, upper=0)),
                    raises(MultRangeError))

    def test_dump_and_load_yaml_should_succeed(self):
        obj = Type()
        data = "!Type {}\n"
        assert_that(yaml.dump(obj, default_flow_style=False), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))
