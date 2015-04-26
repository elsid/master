# coding: utf-8

from plyj.model import (
    Visitor, MethodDeclaration, ClassDeclaration, InterfaceDeclaration,
    EnumDeclaration, InstanceCreation)
from uml_matcher import Dependency
from java_parser.full_classifiers_names import get_name_value


class DependenciesFactory(Visitor):
    def __init__(self, types):
        super(DependenciesFactory, self).__init__()
        self.types = types
        self.dependencies = []
        self.__chain = []

    def visit_Type(self, declaration):
        if not self.__in_method_body() and not self.__in_instance_creation():
            return
        type_name = get_name_value(declaration.name)
        if type_name not in self.types:
            return
        supplier = self.types[type_name].classifier
        dependency = Dependency(client=self.__current_classifier(),
                                supplier=supplier)
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_ClassDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_InterfaceDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def visit_EnumDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_EnumDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def visit_MethodDeclaration(self, declaration):
        self.__chain.append(declaration)
        return True

    def leave_MethodDeclaration(self, _):
        self.__chain.pop()

    def visit_InstanceCreation(self, declaration):
        self.__chain.append(declaration)
        return True

    def leave_InstanceCreation(self, _):
        self.__chain.pop()

    def __visit_classifier(self, declaration):
        self.__chain.append(declaration)
        return True

    def __leave_classifier(self, _):
        self.__chain.pop()

    def __in_method_body(self):
        return (isinstance(self.__chain[-1], MethodDeclaration)
                if self.__chain else False)

    def __in_instance_creation(self):
        return (isinstance(self.__chain[-1], InstanceCreation)
                if self.__chain else False)

    def __current_classifier(self):
        classifiers = (ClassDeclaration, InterfaceDeclaration, EnumDeclaration)
        for declaration in reversed(self.__chain):
            if isinstance(declaration, classifiers):
                return self.types[declaration.name].classifier


def make_dependencies(tree, types):
    factory = DependenciesFactory(types)
    tree.accept(factory)
    return factory.dependencies
