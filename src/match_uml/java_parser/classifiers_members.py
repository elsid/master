# coding: utf-8

from plyj.model import Visitor, Type as PlyjType

from uml_matcher import (
    Property, Operation, DataType, Visibility, Type, Parameter, PrimitiveType)
from java_parser.full_classifiers_names import get_name_value
from java_parser.errors import (
    MethodRedeclaration, VariableRedeclaration, FieldModifiersDuplication,
    MethodModifiersDuplication, FormalParameterModifiersDuplication,
    PlyjDeclarationTypeError)


PRIMITIVE_TYPES = frozenset(('void', 'byte', 'short', 'int', 'long', 'float',
                             'double', 'boolean', 'char'))


def get_visibility(declaration):
    if 'public' in declaration.modifiers:
        return Visibility.public
    elif 'protected' in declaration.modifiers:
        return Visibility.protected
    else:
        return Visibility.private


def has_duplications(values):
    return len(values) != len(set(values))


def format_type_arguments(type_arguments):
    return '<>' if type_arguments else ''


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


class ClassifiersChainLink(object):
    def __init__(self, classifier):
        self.classifier = classifier
        self.operation = None


class ClassifiersMembersFactory(Visitor):
    __field = None

    def __init__(self, classifiers):
        super(ClassifiersMembersFactory, self).__init__()
        self.errors = []
        self.classifiers = classifiers
        self.__classifiers_chain = []
        self.__visited_classifiers = set()
        self.types = dict((c.name, Type(c)) for c in classifiers.values())

    def visit_ClassDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_ClassDeclaration(self, declaration):
        self.__leave_classifier(declaration)

    def visit_InterfaceDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_InterfaceDeclaration(self, declaration):
        self.__leave_classifier(declaration)

    def visit_EnumDeclaration(self, declaration):
        return self.__visit_classifier(declaration)

    def leave_EnumDeclaration(self, declaration):
        self.__leave_classifier(declaration)

    def visit_FieldDeclaration(self, declaration):
        self.__field = declaration
        if has_duplications(self.__field.modifiers):
            self.errors.append(FieldModifiersDuplication(
                self.__current_classifier(), self.__field))
            return False
        return True

    def leave_FieldDeclaration(self, _):
        self.__field = None

    def visit_VariableDeclarator(self, declaration):
        classifier = self.__current_classifier()
        if classifier.has_property(declaration.variable.name):
            self.errors.append(VariableRedeclaration(classifier,
                                                     declaration.variable))
            return False
        if self.__field:
            classifier.properties.append(Property(
                type=self.__get_classifier_type(VariableType(
                    self.__field, declaration.variable)),
                name=declaration.variable.name,
                visibility=get_visibility(self.__field),
                is_static='static' in self.__field.modifiers,
                owner=classifier,
            ))
            return True

    def visit_MethodDeclaration(self, declaration):
        if self.__current_operation():
            return False
        if has_duplications(declaration.modifiers):
            self.errors.append(MethodModifiersDuplication(
                self.__current_classifier(), declaration))
            return False
        self.__set_operation(Operation(
            name=declaration.name,
            visibility=get_visibility(declaration),
            result=self.__get_classifier_type(MethodReturnType(declaration)),
            parameters=[],
            is_static='static' in declaration.modifiers,
        ))
        return True

    def leave_MethodDeclaration(self, declaration):
        operation = self.__current_operation()
        if declaration.name != operation.name:
            return
        classifier = self.__current_classifier()
        if operation in classifier.operations:
            self.errors.append(MethodRedeclaration(operation, classifier,
                                                   declaration))
        else:
            classifier.operations.append(operation)
        self.__reset_operation()

    def visit_FormalParameter(self, declaration):
        if has_duplications(declaration.modifiers):
            self.errors.append(FormalParameterModifiersDuplication(
                self.__current_operation(), self.__current_classifier(),
                declaration))
            return False
        operation = self.__current_operation()
        if operation:
            operation.parameters.append(Parameter(
                type=self.__get_classifier_type(
                    FormalParameterType(declaration)),
                name=declaration.variable.name,
            ))
            return True

    def visit_EnumConstant(self, _):
        return False

    def visit_InstanceCreation(self, _):
        return False

    def __get_classifier_type(self, declaration_type):
        classifier_name = declaration_type.classifier_name()
        if classifier_name not in self.classifiers:
            self.classifiers[classifier_name] = (
                PrimitiveType(classifier_name)
                if classifier_name in PRIMITIVE_TYPES
                else DataType(classifier_name))
        type_name = declaration_type.type_name()
        if type_name not in self.types:
            classifier = self.classifiers[classifier_name]
            self.types[type_name] = declaration_type.type(classifier)
        return self.types[type_name]

    def __visit_classifier(self, declaration):
        if declaration.name in self.__visited_classifiers:
            return False
        self.__visited_classifiers.add(declaration.name)
        classifier = self.classifiers[declaration.name]
        self.__classifiers_chain.append(ClassifiersChainLink(classifier))
        return True

    def __leave_classifier(self, declaration):
        if declaration.name == self.__current_classifier().name:
            self.__classifiers_chain.pop()

    def __last_link(self):
        return self.__classifiers_chain[-1]

    def __current_classifier(self):
        return self.__last_link().classifier

    def __current_operation(self):
        return self.__last_link().operation

    def __set_operation(self, operation):
        self.__last_link().operation = operation

    def __reset_operation(self):
        self.__set_operation(None)


def fill_classifiers(tree, classifiers):
    factory = ClassifiersMembersFactory(classifiers)
    tree.accept(factory)
    return factory.types, factory.errors
