# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.primitive_type import PrimitiveType


class MakeDataType(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(PrimitiveType()), equal_to('primitive type anonymous'))
        assert_that(str(PrimitiveType('A')), equal_to('primitive type A'))

    def test_repr_should_succeed(self):
        assert_that(repr(PrimitiveType()),
                    equal_to("PrimitiveType('anonymous')"))
        assert_that(repr(PrimitiveType('A')), equal_to("PrimitiveType('A')"))


if __name__ == '__main__':
    main()