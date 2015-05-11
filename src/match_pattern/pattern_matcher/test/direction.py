# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from pattern_matcher.direction import Direction


class MakeDirection(TestCase):
    def test_make(self):
        assert_that(str(Direction.IN), equal_to('in'))
        assert_that(str(Direction.OUT), equal_to('out'))
        assert_that(str(Direction.INOUT), equal_to('inout'))

    def test_yaml_dump(self):
        assert_that(yaml.dump(Direction.IN),
                    equal_to("!Direction 'in'\n"))
        assert_that(yaml.dump(Direction.OUT),
                    equal_to("!Direction 'out'\n"))
        assert_that(yaml.dump(Direction.INOUT),
                    equal_to("!Direction 'inout'\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Direction 'in'\n"),
                    equal_to(Direction.IN))
        assert_that(yaml.load("!Direction 'out'\n"),
                    equal_to(Direction.OUT))
        assert_that(yaml.load("!Direction 'inout'\n"),
                    equal_to(Direction.INOUT))


if __name__ == '__main__':
    main()
