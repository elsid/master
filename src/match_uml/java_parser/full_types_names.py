# coding: utf-8

from plyj.model import Visitor
from java_parser.full_classifiers_names import get_name_value
from java_parser.external_classifiers import FORCE_IMPORT
from java_parser.errors import TypeNameNotFound, AmbiguousTypeName


class SetFullTypesNames(Visitor):
    __package = None

    def __init__(self, classifiers):
        super(SetFullTypesNames, self).__init__()
        self.errors = []
        self.__classifiers = classifiers
        self.__visible_classifiers = {}
        for force_import in FORCE_IMPORT:
            for classifier in classifiers.itervalues():
                if classifier.name.startswith(force_import):
                    self.__visible_classifiers[classifier.name] = classifier
        self.__classifiers_chain = []

    def visit_PackageDeclaration(self, declaration):
        self.__package = get_name_value(declaration.name)
        self.__add_visible_from(self.__package)

    def visit_ImportDeclaration(self, declaration):
        self.__add_visible_from(get_name_value(declaration.name))

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_ClassDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_InterfaceDeclaration(self, declaration):
        return self.__leave_classifier(declaration)

    def visit_Type(self, declaration):
        type_name = declaration.name.value
        subclassifier_name = '$'.join((self.__classifiers_chain[-1], type_name))
        if subclassifier_name in self.__visible_classifiers:
            declaration.name.value = subclassifier_name
        else:
            classifiers_names = tuple(self.__find_classifiers_names(type_name))
            if not classifiers_names:
                self.__add_error_type_not_found(declaration)
            elif len(classifiers_names) > 1:
                self.__add_error_ambiguous_type_name(declaration)
            else:
                declaration.name.value = classifiers_names[0]

    def __add_visible_from(self, prefix):
        for classifier_name, classifier in self.__classifiers.iteritems():
            if classifier_name.startswith(prefix):
                self.__visible_classifiers[classifier_name] = classifier

    def __visit_classifier(self, declaration):
        name = get_name_value(declaration.name)
        self.__classifiers_chain.append(name)
        return True

    def __leave_classifier(self, _):
        self.__classifiers_chain.pop()
        return True

    def __find_classifiers_names(self, type_name):
        for name in self.__visible_classifiers.iterkeys():
            if name.endswith(type_name):
                yield name

    def __add_error_type_not_found(self, declaration):
        classifier = self.__classifiers[self.__classifiers_chain[-1]]
        self.errors.append(TypeNameNotFound(classifier, declaration))

    def __add_error_ambiguous_type_name(self, declaration):
        classifier = self.__classifiers[self.__classifiers_chain[-1]]
        self.errors.append(AmbiguousTypeName(classifier, declaration))


def set_full_types_names(tree, classifiers):
    factory = SetFullTypesNames(classifiers)
    tree.accept(factory)
    return factory.errors
