# coding: utf-8

from hamcrest import assert_that, empty
from java_parser.full_types_names import set_full_types_names
from java_parser.test.classifiers import TestCaseWithParser


class SetFullTypeNames(TestCaseWithParser):
    def test_set_empty_should_succeed(self):
        assert_that(set_full_types_names(self.parse(''), {}), empty())
