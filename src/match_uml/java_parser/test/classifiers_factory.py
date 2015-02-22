#coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from plyj.parser import Parser
from plyj.model import ClassDeclaration, InterfaceDeclaration
from uml_matcher import Class, Interface
from java_parser.classifiers_factory import (make_class, make_interface,
    make_classifiers)

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
        classifiers = make_classifiers(tree)
        assert_that(classifiers, equal_to({}))

    def test_make_one_class_should_succeed(self):
        tree = self.parse('class C {}')
        classifiers = make_classifiers(tree)
        assert_that(classifiers, equal_to({'C': Class('C')}))

    def test_make_one_interface_should_succeed(self):
        tree = self.parse('interface I {}')
        classifiers = make_classifiers(tree)
        assert_that(classifiers, equal_to({'I': Interface('I')}))

    def test_make_several_class_should_succeed(self):
        tree = self.parse('''
            class C1 {}
            class C2 {}
            interface I1 {}
            interface I2 {}
        ''')
        classifiers = make_classifiers(tree)
        assert_that(classifiers, equal_to({
            'C1': Class('C1'),
            'C2': Class('C2'),
            'I1': Interface('I1'),
            'I2': Interface('I2')
        }))

if __name__ == '__main__':
    main()
