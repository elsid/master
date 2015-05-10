# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.direction import Direction


class MakeDirection(TestCase):
    def test_make(self):
        assert_that(str(Direction.in_), equal_to('in'))
        assert_that(str(Direction.out), equal_to('out'))
        assert_that(str(Direction.inout), equal_to('inout'))

    def test_yaml_dump(self):
        assert_that(yaml.dump(Direction.in_),
                    equal_to("!Direction 'in'\n"))
        assert_that(yaml.dump(Direction.out),
                    equal_to("!Direction 'out'\n"))
        assert_that(yaml.dump(Direction.inout),
                    equal_to("!Direction 'inout'\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Direction 'in'\n"),
                    equal_to(Direction.in_))
        assert_that(yaml.load("!Direction 'out'\n"),
                    equal_to(Direction.out))
        assert_that(yaml.load("!Direction 'inout'\n"),
                    equal_to(Direction.inout))


if __name__ == '__main__':
    main()
