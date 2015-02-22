#coding: utf-8

from plyj.model import Visitor
from uml_matcher.diagram import Generalization

class GeneralizationsFactory(Visitor):
    def __init__(self, classifiers):
        super().__init__()
        self.classifiers = classifiers
        self.generalizations = []

    def visit_ClassDeclaration(self, declaration):
        self.visit_extended(declaration)
        self.visit_implementation(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        self.visit_extended(declaration)

    def visit_extended(self, declaration):
        derived = self.classifiers[declaration.name]
        if declaration.extends:
            self.generalizations.append(Generalization(derived=derived,
                base=self.classifiers[declaration.extends.name.value]))

    def visit_implementation(self, declaration):
        derived = self.classifiers[declaration.name]
        for base_declaration in declaration.implements:
            self.generalizations.append(Generalization(derived=derived,
                base=self.classifiers[base_declaration.name.value]))

def make_generalizations(tree, classifiers):
    factory = GeneralizationsFactory(classifiers)
    tree.accept(factory)
    return factory.generalizations
