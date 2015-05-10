# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from uml_matcher.enumeration import Enumeration


class MakeEnumeration(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Enumeration()), starts_with('enumeration anonymous_'))
        assert_that(str(Enumeration('A')), equal_to('enumeration A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Enumeration('A')), equal_to("Enumeration('A')"))


if __name__ == '__main__':
    main()
