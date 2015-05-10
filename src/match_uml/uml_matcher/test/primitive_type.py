# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from uml_matcher.primitive_type import PrimitiveType


class MakePrimitiveType(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(PrimitiveType()),
                    starts_with('primitive type anonymous_'))
        assert_that(str(PrimitiveType('A')), equal_to('primitive type A'))

    def test_repr_should_succeed(self):
        assert_that(repr(PrimitiveType('A')), equal_to("PrimitiveType('A')"))


if __name__ == '__main__':
    main()
