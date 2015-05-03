# coding: utf-8

from plyj.model import Visitor


class GeneralizationsFactory(Visitor):
    def __init__(self, classifiers):
        super(GeneralizationsFactory, self).__init__()
        self.classifiers = classifiers

    def visit_ClassDeclaration(self, declaration):
        if declaration.extends:
            self.__make_generalizations(declaration, (declaration.extends,))
        self.__make_generalizations(declaration, declaration.implements)

    def visit_InterfaceDeclaration(self, declaration):
        self.__make_generalizations(declaration, declaration.extends)

    def visit_EnumDeclaration(self, declaration):
        self.__make_generalizations(declaration, declaration.implements)

    def __make_generalizations(self, declaration, general_declarations):
        derived = self.classifiers[declaration.name]
        for general_declaration in general_declarations:
            if general_declaration.name.value in self.classifiers:
                general = self.classifiers[general_declaration.name.value]
                if general not in derived.generals:
                    derived.generals.append(general)


def make_generalizations(tree, classifiers):
    factory = GeneralizationsFactory(classifiers)
    tree.accept(factory)
