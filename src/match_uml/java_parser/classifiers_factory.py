#coding: utf-8

from plyj.model import Visitor
Class = __import__('uml_matcher.class', fromlist=['Class']).Class
from uml_matcher.interface import Interface

def make_class(declaration):
    return Class(declaration.name)

def make_interface(declaration):
    return Interface(declaration.name)

class ClassifiersFactory(Visitor):
    def __init__(self):
        self.classifiers = {}
        super().__init__()

    def visit_ClassDeclaration(self, declaration):
        self.classifiers[declaration.name] = make_class(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        self.classifiers[declaration.name] = make_interface(declaration)

def make_classifiers(tree):
    factory = ClassifiersFactory()
    tree.accept(factory)
    return factory.classifiers
