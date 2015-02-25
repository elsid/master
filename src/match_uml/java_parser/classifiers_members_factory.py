# coding: utf-8

from plyj.model import Visitor, Type as PlyjType, Name as PlyjName

from uml_matcher import (
    Property, Operation, DataType, Visibility, Type, Parameter)
from java_parser.errors import (
    MethodRedeclaration, VariableRedeclaration, FieldModifiersDuplication,
    MethodModifiersDuplication, FormalParameterModifiersDuplication,
    PlyjDeclarationTypeError, PlyjNameTypeError)


def get_visibility(declaration):
    if 'public' in declaration.modifiers:
        return Visibility.public
    elif 'protected' in declaration.modifiers:
        return Visibility.protected
    else:
        return Visibility.private


def has_duplications(values):
    return len(values) != len(set(values))


def get_name_value(name):
    if isinstance(name, str):
        return name
    elif isinstance(name, PlyjName):
        return name.value
    else:
        raise PlyjNameTypeError(name)


def format_type_arguments(type_arguments):
    args = ', '.join(get_type_name(t) for t in type_arguments)
    return '<%s>' % args if args else ''


def get_type_name(declaration_type, add_dimensions=0):
    if isinstance(declaration_type, str):
        return declaration_type
    elif isinstance(declaration_type, PlyjType):
        return (get_name_value(declaration_type.name)
                + format_type_arguments(declaration_type.type_arguments)
                + '[]' * (declaration_type.dimensions + add_dimensions))
    else:
        raise PlyjDeclarationTypeError(declaration_type)


def get_classifier_name(declaration_type):
    if isinstance(declaration_type, PlyjType):
        return get_name_value(declaration_type.name)
    else:
        return get_type_name(declaration_type)


def get_dimensions(declaration_type):
    return (declaration_type.dimensions
            if isinstance(declaration_type, PlyjType) else 0)


class VariableType(object):
    def __init__(self, field, variable):
        self.field = field
        self.variable = variable

    def type(self, classifier):
        mult_lower, mult_upper = ((0, None) if get_dimensions(self.field.type)
                                  + self.variable.dimensions else (1, 1))
        return Type(classifier, mult_lower, mult_upper)

    def type_name(self):
        return get_type_name(self.field.type, self.variable.dimensions)

    def classifier_name(self):
        return get_classifier_name(self.field.type)


class MethodReturnType(object):
    def __init__(self, method):
        self.method = method

    def type(self, classifier):
        mult_lower, mult_upper = (
            (0, None) if get_dimensions(self.method.return_type)
            + self.method.extended_dims else (1, 1))
        return Type(classifier, mult_lower, mult_upper)

    def type_name(self):
        return get_type_name(self.method.return_type, self.method.extended_dims)

    def classifier_name(self):
        return get_classifier_name(self.method.return_type)


class FormalParameterType(object):
    def __init__(self, parameter):
        self.parameter = parameter

    def type(self, classifier):
        mult_lower, mult_upper = (
            (0, None) if get_dimensions(self.parameter.type)
            + self.parameter.variable.dimensions else (1, 1))
        return Type(classifier, mult_lower, mult_upper)

    def type_name(self):
        return get_type_name(self.parameter.type,
                             self.parameter.variable.dimensions)

    def classifier_name(self):
        return get_classifier_name(self.parameter.type)


class ClassifiersMembersFactory(Visitor):
    __classifier = None
    __field = None
    __operation = None

    def __init__(self, classifiers):
        super().__init__()
        self.errors = []
        self.classifiers = classifiers
        self.__visited_classifiers = set()
        self.__types = {}

    def visit_ClassDeclaration(self, declaration):
        if declaration.name in self.__visited_classifiers:
            return False
        self.__visited_classifiers.add(declaration.name)
        self.__classifier = self.classifiers[declaration.name]
        return True

    def visit_InterfaceDeclaration(self, declaration):
        if declaration.name in self.__visited_classifiers:
            return False
        self.__visited_classifiers.add(declaration.name)
        self.__classifier = self.classifiers[declaration.name]
        return True

    def visit_FieldDeclaration(self, declaration):
        self.__field = declaration
        if has_duplications(self.__field.modifiers):
            self.errors.append(FieldModifiersDuplication(
                self.__classifier, self.__field))
            return False
        return True

    def visit_VariableDeclarator(self, declaration):
        if self.__classifier.has_property(declaration.variable.name):
            self.errors.append(VariableRedeclaration(self.__classifier,
                                                     declaration.variable))
            return False
        self.__classifier.properties.append(Property(
            type=self.__get_classifier_type(VariableType(self.__field,
                                                         declaration.variable)),
            name=declaration.variable.name,
            visibility=get_visibility(self.__field),
            is_read_only='final' in self.__field.modifiers,
            is_static='static' in self.__field.modifiers,
        ))
        return True

    def visit_MethodDeclaration(self, declaration):
        if self.__classifier.has_operation(declaration.name):
            self.errors.append(MethodRedeclaration(self.__classifier,
                                                   declaration))
            return False
        if has_duplications(declaration.modifiers):
            self.errors.append(MethodModifiersDuplication(
                self.__classifier, declaration))
            return False
        self.__operation = Operation(
            name=declaration.name,
            visibility=get_visibility(declaration),
            result=self.__get_classifier_type(MethodReturnType(declaration)),
            parameters=[],
            is_static='static' in declaration.modifiers,
        )
        self.__classifier.operations.append(self.__operation)
        return True

    def visit_FormalParameter(self, declaration):
        if has_duplications(declaration.modifiers):
            self.errors.append(FormalParameterModifiersDuplication(
                self.__classifier, declaration))
            return False
        self.__operation.parameters.append(Parameter(
            type=self.__get_classifier_type(FormalParameterType(declaration)),
            name=declaration.variable.name,
        ))
        return True

    def __get_classifier_type(self, declaration_type):
        classifier_name = declaration_type.classifier_name()
        if classifier_name not in self.classifiers:
            self.classifiers[classifier_name] = DataType(classifier_name)
        type_name = declaration_type.type_name()
        if type_name not in self.__types:
            classifier = self.classifiers[classifier_name]
            self.__types[type_name] = declaration_type.type(classifier)
        return self.__types[type_name]


def fill_classifiers(tree, classifiers):
    factory = ClassifiersMembersFactory(classifiers)
    tree.accept(factory)
    return factory.errors