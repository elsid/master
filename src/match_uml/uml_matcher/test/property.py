# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.property import Property
from uml_matcher.type import Type
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class MakeProperty(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Property(None)), equal_to('anonymous'))
        assert_that(str(Property(Type(Class('A')), 'x', owner=Class('B'))),
                    equal_to('B::x: A'))


if __name__ == '__main__':
    main()
