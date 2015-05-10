# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.visibility import Visibility


class MakeVisibility(TestCase):
    def test_make(self):
        assert_that(str(Visibility.public), equal_to('+'))
        assert_that(str(Visibility.protected), equal_to('#'))
        assert_that(str(Visibility.private), equal_to('-'))


if __name__ == '__main__':
    main()
