# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with, ends_with
from uml_matcher.operation import Operation
from uml_matcher.type import Type
from uml_matcher.parameter import Parameter
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class MakeOperation(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Operation().sub_equiv_pattern(Operation()), equal_to(True))

    def test_str_should_succeed(self):
        assert_that(str(Operation()),
                    starts_with('anonymous_') and ends_with('()'))
        assert_that(str(Operation(Type(Class('A')), 'f', owner=Class('B'))),
                    equal_to('B::f(): A'))

    def test_dump_and_load_yaml_with_name_should_succeed(self):
        obj = Operation(name='f')
        data = "!Operation {name: f}\n"
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))

    def test_dump_and_load_yaml_with_attrs_and_parameters_should_succeed(self):
        obj = Operation(name='f', is_static=True,
                        parameters=[Parameter(name='x')])
        data = (
            "!Operation\n"
            "is_static: true\n"
            "name: f\n"
            "parameters:\n"
            "- !Parameter {name: x}\n"
        )
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))


if __name__ == '__main__':
    main()
