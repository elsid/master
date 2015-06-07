# coding: utf-8

from plyj.model import Visitor
from pattern_matcher import Class, Interface
from java_source_parser.errors import ClassifierRedeclaration


def make_class(declaration):
    return Class(declaration.name)


def make_interface(declaration):
    return Interface(declaration.name)


class ClassifiersFactory(Visitor):
    def __init__(self):
        super(ClassifiersFactory, self).__init__()
        self.classifiers = {}
        self.errors = []

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration, make_class)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration, make_interface)

    def visit_EnumDeclaration(self, declaration):
        return self.__visit_classifier(declaration, make_class)

    def __visit_classifier(self, declaration, make):
        if declaration.name in self.classifiers:
            self.errors.append(ClassifierRedeclaration(declaration))
            return False
        classifier = make(declaration)
        self.classifiers[declaration.name] = classifier
        return True


def make_classifiers(tree):
    factory = ClassifiersFactory()
    tree.accept(factory)
    return factory.classifiers, factory.errors
