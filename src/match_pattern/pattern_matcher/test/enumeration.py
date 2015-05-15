# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from pattern_matcher.enumeration import Enumeration
from pattern_matcher.property import Property


class MakeEnumeration(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Enumeration()), starts_with('enumeration anonymous_'))
        assert_that(str(Enumeration('A')), equal_to('enumeration A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Enumeration('A')), equal_to("Enumeration('A')"))

    def test_dump_and_load_yaml_enumeration_with_name_should_succeed(self):
        data = "!Enumeration {name: a}\n"
        enumeration = Enumeration('a')
        assert_that(yaml.dump(enumeration), equal_to(data))
        assert_that(yaml.load(data), equal_to(enumeration))

    def test_dump_and_load_yaml_enumeration_with_property_should_succeed(self):
        enumeration = Enumeration('a', properties=[Property(name='a')])
        data = (
            "&id001 !Enumeration\n"
            "name: a\n"
            "properties:\n"
            "- !Property\n"
            "  name: a\n"
            "  owner: *id001\n"
        )
        assert_that(yaml.dump(enumeration), equal_to(data))
        assert_that(yaml.load(data), equal_to(enumeration))

    def test_dump_and_load_yaml_recursive_enumeration_should_succeed(self):
        enumeration = Enumeration('a')
        enumeration.suppliers = [enumeration]
        data = (
            "&id001 !Enumeration\n"
            "name: a\n"
            "suppliers:\n"
            "- *id001\n"
        )
        assert_that(yaml.dump(enumeration), equal_to(data))
        assert_that(yaml.load(data), equal_to(enumeration))


if __name__ == '__main__':
    main()
