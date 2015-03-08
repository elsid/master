# coding: utf-8

from plyj.model import Visitor
from uml_matcher import Class, Interface, Enumeration
from java_parser.errors import (
    ClassRedeclaration, InterfaceRedeclaration, EnumerationRedeclaration)


def make_class(declaration):
    return Class(declaration.name)


def make_interface(declaration):
    return Interface(declaration.name)


def make_enumeration(declaration):
    return Enumeration(declaration.name)


class ClassifiersFactory(Visitor):
    def __init__(self):
        super(ClassifiersFactory, self).__init__()
        self.classifiers = {}
        self.errors = []

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration, make_class,
                                       ClassRedeclaration)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration, make_interface,
                                       InterfaceRedeclaration)

    def visit_EnumDeclaration(self, declaration):
        return self.__visit_classifier(declaration, make_enumeration,
                                       EnumerationRedeclaration)

    def __visit_classifier(self, declaration, make, redeclaration_error):
        if declaration.name in self.classifiers:
            self.errors.append(redeclaration_error(declaration))
            return False
        classifier = make(declaration)
        self.classifiers[declaration.name] = classifier
        return True


def make_classifiers(tree):
    factory = ClassifiersFactory()
    tree.accept(factory)
    return factory.classifiers, factory.errors
