# coding: utf-8

from hamcrest import assert_that, equal_to, empty
from unittest import main
from pattern_matcher import Class, Interface
from java_source_parser.classifiers import make_classifiers
from java_source_parser.generalizations import make_generalizations
from java_source_parser.test.classifiers import TestCaseWithParser


class MakeGeneralizations(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        make_generalizations(tree, classifiers)

    def test_make_class_extends_class_should_succeed(self):
        tree = self.parse('''
            class General {}
            class Derived extends General {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        make_generalizations(tree, classifiers)
        assert_that(classifiers['Derived'].generals, equal_to([
            Class('General'),
        ]))

    def test_make_class_implements_two_interfaces_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            class Realization implements InterfaceA, InterfaceB {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        make_generalizations(tree, classifiers)
        assert_that(classifiers['Realization'].generals, equal_to([
            Interface('InterfaceA'),
            Interface('InterfaceB'),
        ]))

    def test_make_interface_extends_two_interfaces_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            interface InterfaceC extends InterfaceA, InterfaceB {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        make_generalizations(tree, classifiers)
        assert_that(classifiers['InterfaceC'].generals, equal_to([
            Interface('InterfaceA'),
            Interface('InterfaceB'),
        ]))

    def test_make_class_extends_and_implements_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            class General {}
            class Realization extends General implements InterfaceA, InterfaceB
            {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        make_generalizations(tree, classifiers)
        assert_that(classifiers['Realization'].generals, equal_to([
            Class('General'),
            Interface('InterfaceA'),
            Interface('InterfaceB'),
        ]))
