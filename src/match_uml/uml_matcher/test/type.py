# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, calling, raises, equal_to
from uml_matcher.type import Type, repr_multiplicity
Class = __import__('uml_matcher.class', fromlist=['Class']).Class
from uml_matcher.errors import (
    MultLowerTypeError, MultUpperTypeError, NegativeMultLower,
    NegativeMultUpper, MultRangeError)


class ReprMultiplicity(TestCase):
    def test_different_combinations_should_succeed(self):
        assert_that(repr_multiplicity(None, None), equal_to(''))
        assert_that(repr_multiplicity(42, None), equal_to('[42..*]'))
        assert_that(repr_multiplicity(None, 42), equal_to('[42]'))
        assert_that(repr_multiplicity(13, 42), equal_to('[13..42]'))
        assert_that(repr_multiplicity(1, 1), equal_to(''))


class MakeType(TestCase):
    def test_sub_equivalent_pattern_should_succeed(self):
        assert_that(Type(Class()).sub_equiv_pattern(Type(Class())),
                    equal_to(True))

    def test_equivalent_pattern_mult_range_should_succeed(self):
        assert_that(Type(Class()).equivalent_pattern_mult_range(Type(Class())),
                    equal_to(True))

    def test_eq_should_succeed(self):
        assert_that(Type(Class()), equal_to(Type(Class())))

    def test_repr_should_succeed(self):
        assert_that(repr(Type(Class())), equal_to('anonymous'))

    def test_make_with_wrong_lower_should_throw_exception(self):
        assert_that(calling(lambda: Type(None, mult_lower='')),
                    raises(MultLowerTypeError))
        assert_that(calling(lambda: Type(None, mult_lower=-1)),
                    raises(NegativeMultLower))

    def test_make_with_wrong_upper_should_throw_exception(self):
        assert_that(calling(lambda: Type(None, mult_upper='')),
                    raises(MultUpperTypeError))
        assert_that(calling(lambda: Type(None, mult_upper=-1)),
                    raises(NegativeMultUpper))

    def test_make_with_wrong_range_should_throw_exception(self):
        assert_that(calling(lambda: Type(None, mult_lower=1, mult_upper=0)),
                    raises(MultRangeError))

