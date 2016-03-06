# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from pattern_matcher.property import Property
from pattern_matcher.type import Type
Class = __import__('pattern_matcher.class', fromlist=['Class']).Class


class MakeProperty(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Property()), starts_with('anonymous_'))
        assert_that(str(Property('x', Type(Class('A')), owner=Class('B'))),
                    equal_to('B::x: A'))

    def test_dump_and_load_yaml_with_name_should_succeed(self):
        obj = Property('a')
        data = "!Property {name: a}\n"
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))

    def test_dump_and_load_yaml_with_attributes_should_succeed(self):
        obj = Property('a', is_static=False)
        data = "!Property {is_static: false, name: a}\n"
        assert_that(yaml.dump(obj), equal_to(data))
        assert_that(yaml.load(data), equal_to(obj))
