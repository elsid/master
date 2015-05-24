# coding: utf-8

from hamcrest import assert_that, empty
from unittest import main
from java_source_parser.full_types_names import set_full_types_names
from java_source_parser.test.classifiers import TestCaseWithParser


class SetFullTypeNames(TestCaseWithParser):
    def test_set_empty_should_succeed(self):
        assert_that(set_full_types_names(self.parse(''), {}), empty())

if __name__ == '__main__':
    main()
