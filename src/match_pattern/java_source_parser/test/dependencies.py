# coding: utf-8

from hamcrest import assert_that, empty, equal_to
from unittest import main
from java_source_parser.classifiers import make_classifiers
from java_source_parser.full_classifiers_names import set_full_classifiers_names
from java_source_parser.full_types_names import set_full_types_names
from java_source_parser.classifiers_members import fill_classifiers
from java_source_parser.dependencies import make_dependencies
from java_source_parser.test.classifiers import TestCaseWithParser


class MakeDependencies(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        make_dependencies(tree, [])

    def test_make_from_type_method_should_succeed(self):
        tree = self.parse('''
            package x;
            interface Interface {}
            class Implementation implements Interface {}
            class AnotherImplementation implements Interface {}
            class Parameter {}
            class Client {
                Interface field = new Implementation();
                void f(Parameter p) {
                    Interface local = new AnotherImplementation();
                }
            }
        ''')
        set_full_classifiers_names(tree)
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        errors = set_full_types_names(tree, classifiers)
        assert_that(errors, empty())
        types, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        make_dependencies(tree, types)
        assert_that(classifiers['x.Client'].suppliers, equal_to([
            classifiers['x.Implementation'],
            classifiers['x.Parameter'],
            classifiers['x.Interface'],
            classifiers['x.AnotherImplementation'],
        ]))

if __name__ == '__main__':
    main()
