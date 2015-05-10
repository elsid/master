# coding: utf-8

import yaml
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

    def test_dump_and_load_yaml_recursive_primitive_type_should_succeed(self):
        primitive_type = PrimitiveType('a')
        primitive_type.suppliers = [primitive_type]
        data = "&id001 !PrimitiveType\nname: a\nsuppliers:\n- *id001\n"
        assert_that(yaml.dump(primitive_type), equal_to(data))
        assert_that(yaml.load(data), equal_to(primitive_type))


if __name__ == '__main__':
    main()
