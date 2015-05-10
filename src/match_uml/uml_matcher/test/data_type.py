# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from uml_matcher.data_type import DataType


class MakeDataType(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(DataType()), starts_with('data type anonymous_'))
        assert_that(str(DataType('A')), equal_to('data type A'))

    def test_repr_should_succeed(self):
        assert_that(repr(DataType('A')), equal_to("DataType('A')"))

    def test_dump_and_load_yaml_recursive_primitive_type_should_succeed(self):
        primitive_type = DataType('a')
        primitive_type.suppliers = [primitive_type]
        data = "&id001 !DataType\nname: a\nsuppliers:\n- *id001\n"
        assert_that(yaml.dump(primitive_type), equal_to(data))
        assert_that(yaml.load(data), equal_to(primitive_type))


if __name__ == '__main__':
    main()
