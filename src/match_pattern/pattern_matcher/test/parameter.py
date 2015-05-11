# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from pattern_matcher.parameter import Parameter
from pattern_matcher.type import Type
from pattern_matcher.direction import Direction
Class = __import__('pattern_matcher.class', fromlist=['Class']).Class


class MakeParameter(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Parameter()), starts_with('anonymous_'))
        assert_that(str(Parameter(Type(Class('A')), 'x')), equal_to('x: A'))

    def test_dump_and_load_yaml_with_name_should_succeed(self):
        obj = Parameter(name='a')
        data = "!Parameter {name: a}\n"
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))

    def test_dump_and_load_yaml_with_unicode_name_should_succeed(self):
        obj = Parameter(name=u'a')
        data = "!Parameter {name: a}\n"
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))

    def test_dump_and_load_yaml_with_name_and_direction_should_succeed(self):
        obj = Parameter(name='a', direction=Direction.IN)
        data = "!Parameter {direction: !Direction 'in', name: a}\n"
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))


if __name__ == '__main__':
    main()
