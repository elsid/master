# coding: utf-8

from plyj.model import Visitor
from uml_matcher import Class, Interface
from java_parser.errors import ClassRedeclaration, InterfaceRedeclaration


def make_class(declaration):
    return Class(declaration.name)


def make_interface(declaration):
    return Interface(declaration.name)


class ClassifiersFactory(Visitor):
    __classifier = None

    def __init__(self):
        super(ClassifiersFactory, self).__init__()
        self.classifiers = {}
        self.errors = []

    def visit_ClassDeclaration(self, declaration):
        if declaration.name in self.classifiers:
            self.errors.append(ClassRedeclaration(declaration))
            return False
        self.__classifier = make_class(declaration)
        self.classifiers[declaration.name] = self.__classifier
        return True

    def visit_InterfaceDeclaration(self, declaration):
        if declaration.name in self.classifiers:
            self.errors.append(InterfaceRedeclaration(declaration))
            return False
        self.__classifier = make_interface(declaration)
        self.classifiers[declaration.name] = self.__classifier
        return True


def make_classifiers(tree):
    factory = ClassifiersFactory()
    tree.accept(factory)
    return factory.classifiers, factory.errors
