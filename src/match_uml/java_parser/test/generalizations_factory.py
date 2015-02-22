#coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from plyj.parser import Parser
Class = __import__('uml_matcher.class', fromlist=['Class']).Class
from uml_matcher.interface import Interface
from uml_matcher.diagram import Generalization
from java_parser.classifiers_factory import make_classifiers
from java_parser.generalizations_factory import make_generalizations
from java_parser.test.classifiers_factory import TestCaseWithParser

class MakeGeneralizations(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        generalizations = make_generalizations(tree, make_classifiers(tree))
        assert_that(generalizations, equal_to([]))

    def test_make_from_one_extend_should_succeed(self):
        tree = self.parse('''
            class Base {}
            class Derived extends Base {}
        ''')
        generalizations = make_generalizations(tree, make_classifiers(tree))
        assert_that(generalizations, equal_to(
            [(Class('Derived'), Class('Base'))]))

    def test_make_from_two_implments_should_succeed(self):
        tree = self.parse('''
            interface InterfaceA {}
            interface InterfaceB {}
            class Realization implements InterfaceA, InterfaceB {}
        ''')
        generalizations = make_generalizations(tree, make_classifiers(tree))
        G = Generalization
        assert_that(generalizations, equal_to([
            G(derived=Class('Realization'), base=Interface('InterfaceA')),
            G(derived=Class('Realization'), base=Interface('InterfaceB')),
        ]))

if __name__ == '__main__':
    main()
