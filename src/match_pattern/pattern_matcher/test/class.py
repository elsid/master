# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from pattern_matcher.property import Property
Class = __import__('pattern_matcher.class', fromlist=['Class']).Class


class MakeClass(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Class()), starts_with('class anonymous_'))
        assert_that(str(Class('A')), equal_to('class A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Class('A')), equal_to("Class('A')"))

    def test_dump_and_load_yaml_clazz_with_name_should_succeed(self):
        data = "!Class {name: a}\n"
        clazz = Class('a')
        assert_that(yaml.dump(clazz), equal_to(data))
        assert_that(yaml.load(data), equal_to(clazz))

    def test_dump_and_load_yaml_clazz_with_property_should_succeed(self):
        clazz = Class('a', properties=[Property(name='a')])
        data = (
            "&id001 !Class\n"
            "name: a\n"
            "properties:\n"
            "- !Property\n"
            "  name: a\n"
            "  owner: *id001\n"
        )
        assert_that(yaml.dump(clazz), equal_to(data))
        assert_that(yaml.load(data), equal_to(clazz))

    def test_dump_and_load_yaml_recursive_clazz_should_succeed(self):
        clazz = Class('a')
        clazz.suppliers = [clazz]
        data = (
            "&id001 !Class\n"
            "name: a\n"
            "suppliers:\n"
            "- *id001\n"
        )
        assert_that(yaml.dump(clazz), equal_to(data))
        assert_that(yaml.load(data), equal_to(clazz))
