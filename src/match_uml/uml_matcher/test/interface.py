# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.interface import Interface


class MakeInterface(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Interface()), equal_to('interface anonymous'))
        assert_that(str(Interface('A')), equal_to('interface A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Interface()), equal_to("Interface('anonymous')"))
        assert_that(repr(Interface('A')), equal_to("Interface('A')"))


if __name__ == '__main__':
    main()
