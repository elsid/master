# coding: utf-8

from unittest import main
from hamcrest import assert_that, equal_to
from uml_matcher import Class, Interface
from uml_matcher.diagram import Generalization
from java_parser.classifiers_factory import make_classifiers
from java_parser.generalizations_factory import make_generalizations
from java_parser.test.classifiers_factory import TestCaseWithParser


class MakeGeneralizations(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, equal_to([]))
        generalizations = make_generalizations(tree, classifiers)
        assert_that(generalizations, equal_to([]))

    def test_make_class_extends_by_class_should_succeed(self):
        tree = self.parse('''
            class Base {}
            class Derived extends Base {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, equal_to([]))
        generalizations = make_generalizations(tree, classifiers)
        assert_that(generalizations, equal_to(
            [(Class('Derived'), Class('Base'))]))

    def test_make_class_implements_two_interfaces_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            class Realization implements InterfaceA, InterfaceB {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, equal_to([]))
        generalizations = make_generalizations(tree, classifiers)
        G = Generalization
        assert_that(generalizations, equal_to([
            G(derived=Class('Realization'), base=Interface('InterfaceA')),
            G(derived=Class('Realization'), base=Interface('InterfaceB')),
        ]))

if __name__ == '__main__':
    main()
