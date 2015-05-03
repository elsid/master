# coding: utf-8

from hamcrest import assert_that, equal_to, empty, contains_inanyorder
from unittest import main
from uml_matcher import Class, Interface
from uml_matcher.diagram import Generalization
from java_parser.classifiers import make_classifiers
from java_parser.generalizations import make_generalizations
from java_parser.test.classifiers import TestCaseWithParser


class MakeGeneralizations(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        generalizations = make_generalizations(tree, classifiers)
        assert_that(generalizations, empty())

    def test_make_class_extends_class_should_succeed(self):
        tree = self.parse('''
            class General {}
            class Derived extends General {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        generalizations = make_generalizations(tree, classifiers)
        assert_that(generalizations, equal_to(
            [(Class('Derived'), Class('General'))]))

    def test_make_class_implements_two_interfaces_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            class Realization implements InterfaceA, InterfaceB {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        generalizations = make_generalizations(tree, classifiers)
        G = Generalization
        assert_that(generalizations, equal_to([
            G(derived=Class('Realization'), general=Interface('InterfaceA')),
            G(derived=Class('Realization'), general=Interface('InterfaceB')),
        ]))

    def test_make_interface_extends_two_interfaces_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            interface InterfaceC extends InterfaceA, InterfaceB {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        generalizations = make_generalizations(tree, classifiers)
        G = Generalization
        assert_that(generalizations, contains_inanyorder(
            G(derived=Interface('InterfaceC'), general=Interface('InterfaceA')),
            G(derived=Interface('InterfaceC'), general=Interface('InterfaceB')),
        ))

    def test_make_class_extends_and_implements_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            class General {}
            class Realization extends General implements InterfaceA, InterfaceB {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        generalizations = make_generalizations(tree, classifiers)
        G = Generalization
        assert_that(generalizations, contains_inanyorder(
            G(derived=Class('Realization'), general=Class('General')),
            G(derived=Class('Realization'), general=Interface('InterfaceA')),
            G(derived=Class('Realization'), general=Interface('InterfaceB')),
        ))

if __name__ == '__main__':
    main()
