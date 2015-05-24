# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, empty
from plyj.parser import Parser
from plyj.model import ClassDeclaration, InterfaceDeclaration
from pattern_matcher import Class, Interface
from java_source_parser.classifiers import (
    make_class, make_interface, make_classifiers)
from java_source_parser.errors import ClassRedeclaration, InterfaceRedeclaration


class MakeClass(TestCase):
    def test_make_should_succeed(self):
        declaration = ClassDeclaration(name='Class', body=None)
        class_ = make_class(declaration)
        assert_that(class_, equal_to(Class('Class')))


class MakeInterface(TestCase):
    def test_make_should_succeed(self):
        declaration = InterfaceDeclaration(name='Interface', body=None)
        interface = make_interface(declaration)
        assert_that(interface, equal_to(Interface('Interface')))


class TestCaseWithParser(TestCase):
    def setUp(self):
        self.parser = Parser()

    def parse(self, text):
        return self.parser.parse_string(text)


class MakeClassifiers(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        classifiers, errors = make_classifiers(tree)
        assert_that(classifiers, equal_to({}))
        assert_that(errors, empty())

    def test_make_one_class_should_succeed(self):
        tree = self.parse('class C {}')
        classifiers, errors = make_classifiers(tree)
        assert_that(classifiers, equal_to({'C': Class('C')}))
        assert_that(errors, empty())

    def test_make_one_interface_should_succeed(self):
        tree = self.parse('interface I {}')
        classifiers, errors = make_classifiers(tree)
        assert_that(classifiers, equal_to({'I': Interface('I')}))
        assert_that(errors, empty())

    def test_make_several_class_should_succeed(self):
        tree = self.parse('''
            class C1 {}
            class C2 {}
            interface I1 {}
            interface I2 {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(classifiers, equal_to({
            'C1': Class('C1'),
            'C2': Class('C2'),
            'I1': Interface('I1'),
            'I2': Interface('I2'),
        }))
        assert_that(errors, empty())

    def test_declaration_of_two_same_classes_should_return_error(self):
        tree = self.parse('''
            class Class {}
            class Class {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(classifiers, equal_to({'Class': Class('Class')}))
        assert_that(errors, equal_to(
            [ClassRedeclaration(ClassDeclaration('Class', []))]))

    def test_declaration_of_two_same_interfaces_should_return_error(self):
        tree = self.parse('''
            interface Interface {}
            interface Interface {}
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(classifiers, equal_to(
            {'Interface': Interface('Interface')}))
        assert_that(errors, equal_to(
            [InterfaceRedeclaration(InterfaceDeclaration('Interface', []))]))

if __name__ == '__main__':
    main()
