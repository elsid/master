# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to, starts_with
from pattern_matcher.interface import Interface


class MakeInterface(TestCase):
    def test_str_should_succeed(self):
        assert_that(str(Interface()), starts_with('interface anonymous_'))
        assert_that(str(Interface('A')), equal_to('interface A'))

    def test_repr_should_succeed(self):
        assert_that(repr(Interface('A')), equal_to("Interface('A')"))

    def test_dump_and_load_yaml_recursive_interface_should_succeed(self):
        interface = Interface('a')
        interface.suppliers = [interface]
        data = "&id001 !Interface\nname: a\nsuppliers:\n- *id001\n"
        assert_that(yaml.dump(interface), equal_to(data))
        assert_that(yaml.load(data), equal_to(interface))


if __name__ == '__main__':
    main()
