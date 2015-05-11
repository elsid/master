# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from pattern_matcher.visibility import Visibility


class MakeVisibility(TestCase):
    def test_make(self):
        assert_that(str(Visibility.PUBLIC), equal_to('+'))
        assert_that(str(Visibility.PROTECTED), equal_to('#'))
        assert_that(str(Visibility.PRIVATE), equal_to('-'))

    def test_yaml_dump(self):
        assert_that(yaml.dump(Visibility.PUBLIC),
                    equal_to("!Visibility 'public'\n"))
        assert_that(yaml.dump(Visibility.PROTECTED),
                    equal_to("!Visibility 'protected'\n"))
        assert_that(yaml.dump(Visibility.PRIVATE),
                    equal_to("!Visibility 'private'\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Visibility 'public'\n"),
                    equal_to(Visibility.PUBLIC))
        assert_that(yaml.load("!Visibility 'protected'\n"),
                    equal_to(Visibility.PROTECTED))
        assert_that(yaml.load("!Visibility 'private'\n"),
                    equal_to(Visibility.PRIVATE))
        assert_that(yaml.load("!Visibility 'PUBLIC'\n"),
                    equal_to(Visibility.PUBLIC))
        assert_that(yaml.load("!Visibility 'PROTECTED'\n"),
                    equal_to(Visibility.PROTECTED))
        assert_that(yaml.load("!Visibility 'PRIVATE'\n"),
                    equal_to(Visibility.PRIVATE))


if __name__ == '__main__':
    main()
