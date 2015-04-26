# coding: utf-8

from hamcrest import assert_that, empty, contains_inanyorder
from uml_matcher import Dependency
from java_parser.classifiers import make_classifiers
from java_parser.full_classifiers_names import set_full_classifiers_names
from java_parser.full_types_names import set_full_types_names
from java_parser.classifiers_members import fill_classifiers
from java_parser.dependencies import make_dependencies
from java_parser.test.classifiers import TestCaseWithParser


class MakeDependencies(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        dependencies = make_dependencies(tree, [])
        assert_that(dependencies, empty())

    def test_make_from_type_method_should_succeed(self):
        tree = self.parse('''
            package x;
            interface Interface {}
            class Implementation implements Interface {}
            class AnotherImplementation implements Interface {}
            class Client {
                Interface field = new Implementation();
                void f() {
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
        dependencies = make_dependencies(tree, types)
        assert_that(dependencies, contains_inanyorder(
            Dependency(client=classifiers['x.Client'],
                       supplier=classifiers['x.Interface']),
            Dependency(client=classifiers['x.Client'],
                       supplier=classifiers['x.Implementation']),
            Dependency(client=classifiers['x.Client'],
                       supplier=classifiers['x.AnotherImplementation']),
        ))
