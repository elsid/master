# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with, ends_with
from uml_matcher.operation import Operation
from uml_matcher.type import Type
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class MakeOperation(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Operation(None).sub_equiv_pattern(Operation(None)),
                    equal_to(True))

    def test_str_should_succeed(self):
        assert_that(str(Operation(None)),
                    starts_with('anonymous_') and ends_with('()'))
        assert_that(str(Operation(Type(Class('A')), 'f', owner=Class('B'))),
                    equal_to('B::f(): A'))

if __name__ == '__main__':
    main()
