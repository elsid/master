# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that
from graph_matcher.check import check


class Check(TestCase):
    def test_check_empty_should_succeed(self):
        assert_that(check([]))
