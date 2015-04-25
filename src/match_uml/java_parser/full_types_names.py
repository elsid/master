# coding: utf-8

from plyj.model import Visitor, Name as PlyjName, Type as PlyjType
from uml_matcher import PrimitiveType
from java_parser.full_classifiers_names import get_name_value
from java_parser.external_classifiers import FORCE_IMPORT
from java_parser.classifiers_members import PRIMITIVE_TYPES
from java_parser.errors import (
    TypeNameNotFound, AmbiguousTypeName, PlyjNameTypeError)


def set_declaration_name(declaration, name):
    if isinstance(declaration.name, str):
        declaration.name = name
    elif isinstance(declaration.name, PlyjName):
        declaration.name.value = name
    elif isinstance(declaration.name, PlyjType):
        set_declaration_name(declaration.name, name)
    else:
        raise PlyjNameTypeError(declaration.name)


class FindAllClassifiers(Visitor):
    def __init__(self, classifiers):
        super(FindAllClassifiers, self).__init__()
        self.classifiers = classifiers
        self.found_classifiers = {}

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def visit_EnumDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def __visit_classifier(self, declaration):
        classifier = self.classifiers[get_name_value(declaration.name)]
        self.found_classifiers[classifier.name] = classifier
        return True


class SetFullTypesNames(Visitor):
    __package = None

    def __init__(self, classifiers, local_classifiers):
        super(SetFullTypesNames, self).__init__()
        self.errors = []
        self.classifiers = classifiers
        self.visible_classifiers = local_classifiers
        for force_import in FORCE_IMPORT:
            for classifier in classifiers.itervalues():
                if classifier.name.startswith(force_import):
                    self.visible_classifiers[classifier.name] = classifier
        for primitive in PRIMITIVE_TYPES:
            if primitive not in self.classifiers:
                self.classifiers[primitive] = PrimitiveType(primitive)
            self.visible_classifiers[primitive] = self.classifiers[primitive]
        self.__classifiers_chain = []
        self.__imports = set()

    def visit_PackageDeclaration(self, declaration):
        self.__package = get_name_value(declaration.name)
        self.__add_visible_from(self.__package)
        return True

    def visit_ImportDeclaration(self, declaration):
        name = get_name_value(declaration.name)
        self.__imports.add(name)
        self.__add_visible_from(name)
        return True

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

    def visit_Type(self, declaration):
        if not self.__replace_name_for_subclass(declaration):
            self.__replace_name(declaration)
        return True

    def __add_visible_from(self, prefix):
        for classifier_name, classifier in self.classifiers.iteritems():
            if classifier_name.startswith(prefix):
                self.visible_classifiers[classifier_name] = classifier

    def __visit_classifier(self, declaration):
        name = get_name_value(declaration.name)
        self.__classifiers_chain.append(name)
        return True

    def __leave_classifier(self, _):
        self.__classifiers_chain.pop()
        return True

    def __replace_name_for_subclass(self, declaration):
        type_name = get_name_value(declaration.name)
        if self.__classifiers_chain:
            name = '$'.join((self.__classifiers_chain[-1], type_name))
            if name in self.visible_classifiers:
                set_declaration_name(declaration, name)
                return True

    def __replace_name(self, declaration):
        type_name = get_name_value(declaration.name)
        classifiers_names = tuple(self.__find_classifiers_names(type_name))
        if not classifiers_names:
            self.__add_error_type_not_found(declaration)
        elif len(classifiers_names) > 1:
            self.__add_error_ambiguous_type_name(declaration, classifiers_names)
        else:
            set_declaration_name(declaration, classifiers_names[0])

    def __find_classifiers_names(self, type_name):
        package = self.__package

        def is_context_type_name(classifier):
            return classifier == type_name

        def is_this_package_type_name(classifier):
            return package and classifier == package + '.' + type_name

        def is_imported_type_name(classifier):
            return (is_package_type_name(classifier)
                    and classifier in self.__imports)

        def is_package_type_name(classifier):
            return classifier.endswith('.' + type_name)

        def is_sub_type_name(classifier):
            return classifier.endswith('$' + type_name)

        is_type_name_list = (
            is_context_type_name,
            is_this_package_type_name,
            is_imported_type_name,
            is_package_type_name,
            is_sub_type_name,
        )
        result = set()
        for is_type_name in is_type_name_list:
            for name in self.visible_classifiers.iterkeys():
                if name not in result:
                    if is_type_name(name):
                        result.add(name)
                        yield name
            if result:
                return

    def __add_error_type_not_found(self, declaration):
        classifier = self.__current_classifier()
        self.errors.append(TypeNameNotFound(classifier, declaration))

    def __add_error_ambiguous_type_name(self, declaration, candidates):
        classifier = self.__current_classifier()
        self.errors.append(AmbiguousTypeName(classifier, declaration,
                                             candidates))

    def __current_classifier(self):
        return (self.classifiers[self.__classifiers_chain[-1]]
                if self.__classifiers_chain else None)


def set_full_types_names(tree, classifiers):
    find = FindAllClassifiers(classifiers)
    tree.accept(find)
    factory = SetFullTypesNames(classifiers, find.found_classifiers)
    tree.accept(factory)
    return factory.errors
