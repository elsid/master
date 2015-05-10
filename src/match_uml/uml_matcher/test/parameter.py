# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from uml_matcher.parameter import Parameter
from uml_matcher.type import Type
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class MakeParameter(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Parameter()), starts_with('anonymous_'))
        assert_that(str(Parameter(Type(Class('A')), 'x')), equal_to('x: A'))


if __name__ == '__main__':
    main()
