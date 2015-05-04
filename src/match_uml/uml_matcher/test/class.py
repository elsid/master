# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class MakeClass(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Class()), equal_to('class anonymous'))
        assert_that(str(Class('A')), equal_to('class A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Class()), equal_to("Class('anonymous')"))
        assert_that(repr(Class('A')), equal_to("Class('A')"))


if __name__ == '__main__':
    main()
