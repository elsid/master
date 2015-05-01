# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from java_parser.external_classifiers import generate_subpaths


class GenerateSubpaths(TestCase):
    def test_empty_should_succeed(self):
        assert_that(list(generate_subpaths('')), equal_to(['']))

    def test_single_import_should_succeed(self):
        assert_that(list(generate_subpaths('a')), equal_to(['a']))

    def test_multiple_import_should_succeed(self):
        assert_that(list(generate_subpaths('a.b.c')),
                    equal_to(['a$b$c', 'a/b$c', 'a/b/c', 'b$c', 'b/c', 'c']))

if __name__ == '__main__':
    main()
