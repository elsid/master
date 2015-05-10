# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from uml_matcher.interface import Interface


class MakeInterface(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Interface()), starts_with('interface anonymous_'))
        assert_that(str(Interface('A')), equal_to('interface A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Interface('A')), equal_to("Interface('A')"))


if __name__ == '__main__':
    main()
