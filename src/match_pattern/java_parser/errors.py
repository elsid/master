# coding: utf-8

from collections import Counter


class ClassifierTypeError(Exception):
    def __init__(self, classifier):
        super(ClassifierTypeError, self).__init__(
            'unknown classifier type: %s' % type(classifier))


class PlyjDeclarationTypeError(Exception):
    def __init__(self, declaration):
        super(PlyjDeclarationTypeError, self).__init__(
            'not a type of declaration: %s' % type(declaration))


class PlyjNameTypeError(Exception):
    def __init__(self, name):
        super(PlyjNameTypeError, self).__init__(
            'not a name of type: %s' % type(name))


class Error(object):
    def __repr__(self):
        return '{name}(\'{message}\')'.format(name=self.__class__.__name__,
                                              message=str(self))


class PlyjSyntaxError(Error):
    def __init__(self, file_path, message):
        super(PlyjSyntaxError, self).__init__()
        self.file_path = file_path
        self.message = message

    def __str__(self):
        return 'error: {m} in file "{f}"'.format(m=self.message,
                                                 f=self.file_path)

    def __eq__(self, other):
        return (self.file_path == other.file_path
                and self.message == other.message)


class Redeclaration(Error):
    ENTITY = 'entity'

    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return 'error: redeclaration of {entity} {name}'.format(
            entity=self.ENTITY,
            name='"%s"' % self.declaration.name)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Redeclaration)
                and self.ENTITY == other.ENTITY
                and self.declaration == other.declaration)


class ClassRedeclaration(Redeclaration):
    ENTITY = 'class'

    def __init__(self, declaration):
        super(ClassRedeclaration, self).__init__(declaration)

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(ClassRedeclaration, self).__eq__(other)
                and isinstance(other, ClassRedeclaration))


class InterfaceRedeclaration(Redeclaration):
    ENTITY = 'interface'

    def __init__(self, declaration):
        super(InterfaceRedeclaration, self).__init__(declaration)

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(InterfaceRedeclaration, self).__eq__(other)
                and isinstance(other, InterfaceRedeclaration))


class EnumerationRedeclaration(Redeclaration):
    ENTITY = 'enumeration'

    def __init__(self, declaration):
        super(EnumerationRedeclaration, self).__init__(declaration)

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(EnumerationRedeclaration, self).__eq__(other)
                and isinstance(other, EnumerationRedeclaration))


def get_classifier_type_name(classifier):
    from pattern_matcher import Class, Interface, Enumeration

    if isinstance(classifier, Class):
        return 'class'
    elif isinstance(classifier, Interface):
        return 'interface'
    elif isinstance(classifier, Enumeration):
        return 'enumeration'
    else:
        raise ClassifierTypeError(classifier)


class MemberRedeclaration(Redeclaration):
    ENTITY = 'member'

    def __init__(self, classifier, declaration):
        super(MemberRedeclaration, self).__init__(declaration)
        self.classifier = classifier

    def __str__(self):
        return ('error: redeclaration of {entity} {what} in {ctype} '
                '{classifier}'.format(
                    entity=self.ENTITY,
                    what='"%s"' % self._what(),
                    ctype=get_classifier_type_name(self.classifier),
                    classifier='"%s"' % self.classifier.name))

    def _what(self):
        raise NotImplementedError()


class VariableRedeclaration(MemberRedeclaration):
    ENTITY = 'variable'

    def __init__(self, classifier, declaration):
        super(VariableRedeclaration, self).__init__(classifier, declaration)

    def _what(self):
        return self.declaration.name


class MethodRedeclaration(MemberRedeclaration):
    ENTITY = 'method'

    def __init__(self, operation, classifier, declaration):
        super(MethodRedeclaration, self).__init__(classifier, declaration)
        self.operation = operation

    def _what(self):
        return self.operation


class MemberModifiersDuplication(Error):
    def __init__(self, classifier, declaration):
        self.classifier = classifier
        self.declaration = declaration
        self.duplicated_modifiers = sorted(
            (x for x, n in Counter(declaration.modifiers).iteritems() if n > 1))

    def __str__(self):
        return ('error: {prefix} {ctype} {classifier} has duplicated '
                'modifier{mmult}: {modifiers}'.format(
                    prefix=self._prefix(),
                    ctype=get_classifier_type_name(self.classifier),
                    classifier='"%s"' % self.classifier.name,
                    mmult='s' if len(self.duplicated_modifiers) > 1 else '',
                    modifiers=', '.join(self.duplicated_modifiers)))

    def _prefix(self):
        raise NotImplementedError()


class FieldModifiersDuplication(MemberModifiersDuplication):
    def __init__(self, classifier, declaration):
        super(FieldModifiersDuplication, self).__init__(classifier, declaration)

    def _prefix(self):
        vars_decls = self.declaration.variable_declarators
        return ('field variable{fmult} {vars} of'.format(
            fmult='s' if len(vars_decls) > 1 else '',
            vars=', '.join('"%s"' % v.variable.name for v in vars_decls)))


class MethodModifiersDuplication(MemberModifiersDuplication):
    def __init__(self, classifier, declaration):
        super(MethodModifiersDuplication, self).__init__(classifier,
                                                         declaration)

    def _prefix(self):
        return 'method "%s" of' % self.declaration.name


class FormalParameterModifiersDuplication(MemberModifiersDuplication):
    def __init__(self, method, classifier, declaration):
        super(FormalParameterModifiersDuplication, self).__init__(
            classifier, declaration)
        self.method = method

    def _prefix(self):
        return ('formal parameter {param} of method {method} in'.format(
            param='"%s"' % self.declaration.variable.name,
            method='"%s"' % self.method.name))


class TypeNameError(Error):
    def __init__(self, classifier, declaration):
        self.classifier = classifier
        self.declaration = declaration


class TypeNameNotFound(TypeNameError):
    def __init__(self, classifier, declaration):
        super(TypeNameNotFound, self).__init__(classifier, declaration)

    def __str__(self):
        from java_parser.full_classifiers_names import get_name_value
        if self.classifier:
            return ('error: type name {type} used in {classifier} not '
                    'found'.format(
                        type='"%s"' % get_name_value(self.declaration.name),
                        classifier='"%s"' % self.classifier.name))
        return 'error: type name {type} not found'.format(
            type='"%s"' % get_name_value(self.declaration.name))


class AmbiguousTypeName(TypeNameError):
    def __init__(self, classifier, declaration, candidates):
        super(AmbiguousTypeName, self).__init__(classifier, declaration)
        self.candidates = candidates

    def __str__(self):
        from java_parser.full_classifiers_names import get_name_value
        if self.classifier:
            return ('error: type name {type} used in {classifier} is '
                    'ambiguous, candidates are:\n{candidates}').format(
                        type='"%s"' % get_name_value(self.declaration.name),
                        classifier='"%s"' % self.classifier.name,
                        candidates=self.__format_candidates())
        return ('error: type name {type} is ambiguous, candidates are:\n{'
                'candidates}'.format(
                    type='"%s"' % get_name_value(self.declaration.name),
                    candidates=self.__format_candidates()))

    def __format_candidates(self):
        return '\n'.join('%s"%s"' % (4 * ' ', x) for x in self.candidates)


class InvalidPath(Exception):
    def __init__(self, path):
        super(InvalidPath, self).__init__(
            'invalid path: "%s"' % path)
