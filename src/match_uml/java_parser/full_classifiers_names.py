# coding: utf-8

from plyj.model import Visitor, Name as PlyjName
from java_parser.errors import PlyjNameTypeError


def get_name_value(name):
    if isinstance(name, str):
        return name
    elif isinstance(name, PlyjName):
        return name.value
    else:
        raise PlyjNameTypeError(name)


class SetFullClassifiersNames(Visitor):
    __package = None

    def __init__(self):
        super(SetFullClassifiersNames, self).__init__()
        self.__classifiers = []

    def visit_PackageDeclaration(self, declaration):
        self.__package = get_name_value(declaration.name)
        return True

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_ClassDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_InterfaceDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def __visit_classifier(self, declaration):
        name = declaration.name
        self.__set_full_name(declaration)
        self.__classifiers.append(name)
        return True

    def __leave_classifier(self, _):
        self.__classifiers.pop()
        return True

    def __make_full_name(self, name):
        sub_classes = '$'.join(self.__classifiers + [name])
        return (self.__package + '.' + sub_classes
                if self.__package else sub_classes)

    def __set_full_name(self, declaration):
        declaration.name = self.__make_full_name(declaration.name)


def set_full_classifiers_names(tree):
    factory = SetFullClassifiersNames()
    tree.accept(factory)
    return tree
