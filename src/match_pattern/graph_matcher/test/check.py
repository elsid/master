#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from graph_matcher.check import check


class Check(TestCase):
    def test_check_empty_should_succeed(self):
        assert_that(check([]), equal_to(True))


if __name__ == '__main__':
    main()
