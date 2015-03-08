# coding: utf-8

from plyj.model import Visitor
from uml_matcher import Generalization


class GeneralizationsFactory(Visitor):
    def __init__(self, classifiers):
        super(GeneralizationsFactory, self).__init__()
        self.classifiers = classifiers
        self.generalizations = []

    def visit_ClassDeclaration(self, declaration):
        if declaration.extends:
            self.__make_generalizations(declaration, (declaration.extends,))
        self.__make_generalizations(declaration, declaration.implements)

    def visit_InterfaceDeclaration(self, declaration):
        self.__make_generalizations(declaration, declaration.extends)

    def visit_EnumDeclaration(self, declaration):
        self.__make_generalizations(declaration, declaration.implements)

    def __make_generalizations(self, declaration, base_declarations):
        derived = self.classifiers[declaration.name]
        for base_declaration in base_declarations:
            self.generalizations.append(Generalization(
                derived=derived,
                base=self.classifiers[base_declaration.name.value]))


def make_generalizations(tree, classifiers):
    factory = GeneralizationsFactory(classifiers)
    tree.accept(factory)
    return factory.generalizations
