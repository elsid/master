# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from uml_matcher.data_type import DataType


class MakeDataType(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(DataType()), starts_with('data type anonymous_'))
        assert_that(str(DataType('A')), equal_to('data type A'))

    def test_repr_should_succeed(self):
        assert_that(repr(DataType('A')), equal_to("DataType('A')"))


if __name__ == '__main__':
    main()
