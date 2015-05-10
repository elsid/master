# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.visibility import Visibility


class MakeVisibility(TestCase):
    def test_make(self):
        assert_that(str(Visibility.public), equal_to('+'))
        assert_that(str(Visibility.protected), equal_to('#'))
        assert_that(str(Visibility.private), equal_to('-'))

    def test_yaml_dump(self):
        assert_that(yaml.dump(Visibility.public),
                    equal_to("!Visibility 'public'\n"))
        assert_that(yaml.dump(Visibility.protected),
                    equal_to("!Visibility 'protected'\n"))
        assert_that(yaml.dump(Visibility.private),
                    equal_to("!Visibility 'private'\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Visibility 'public'\n"),
                    equal_to(Visibility.public))
        assert_that(yaml.load("!Visibility 'protected'\n"),
                    equal_to(Visibility.protected))
        assert_that(yaml.load("!Visibility 'private'\n"),
                    equal_to(Visibility.private))


if __name__ == '__main__':
    main()
