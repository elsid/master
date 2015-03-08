# coding: utf-8

from collections import Counter


class Error(object):
    pass


class Redeclaration(Error):
    ENTITY = 'entity'

    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return 'redeclaration of {entity} "{name}"'.format(
            entity=self.ENTITY,
            name=self.declaration.name)

    def __repr__(self):
        return '"%s"' % str(self)

    def __eq__(self, other):
        return (self.ENTITY == other.ENTITY
                and self.declaration == other.declaration)


class ClassRedeclaration(Redeclaration):
    ENTITY = 'class'

    def __init__(self, declaration):
        super(ClassRedeclaration, self).__init__(declaration)


class InterfaceRedeclaration(Redeclaration):
    ENTITY = 'interface'

    def __init__(self, declaration):
        super(InterfaceRedeclaration, self).__init__(declaration)


class ClassifierTypeError(Exception):
    def __init__(self, classifier):
        self.classifier = classifier

    def __str__(self):
        return 'Unknown classifier type: %s' % type(self.classifier)


def get_classifier_type_name(classifier):
    from uml_matcher import Class, Interface

    if isinstance(classifier, Class):
        return 'class'
    elif isinstance(classifier, Interface):
        return 'interface'
    else:
        raise ClassifierTypeError(classifier)


class MemberRedeclaration(Redeclaration):
    ENTITY = 'member'

    def __init__(self, classifier, declaration):
        super(MemberRedeclaration, self).__init__(declaration)
        self.classifier = classifier

    def __str__(self):
        return ('redeclaration of {entity} "{name}" in {ctype} "{classifier}"'
                .format(
                    entity=self.ENTITY,
                    name=self.declaration.name,
                    ctype=get_classifier_type_name(self.classifier),
                    classifier=self.classifier))


class VariableRedeclaration(MemberRedeclaration):
    ENTITY = 'variable'

    def __init__(self, classifier, declaration):
        super(VariableRedeclaration, self).__init__(classifier, declaration)


class MethodRedeclaration(MemberRedeclaration):
    ENTITY = 'method'

    def __init__(self, classifier, declaration):
        super(MethodRedeclaration, self).__init__(classifier, declaration)


class MemberModifiersDuplication(Error):
    ENTITY = 'Member'

    def __init__(self, classifier, declaration):
        self.classifier = classifier
        self.declaration = declaration
        self.duplicated_modifiers = sorted(
            (x for x, n in Counter(declaration.modifiers).items() if n > 1))

    def __str__(self):
        return ('{prefix} {ctype} {classifier} has duplicated '
                'modifier{mmult}: {modifiers}'.format(
                    prefix=self._prefix(),
                    ctype=get_classifier_type_name(self.classifier),
                    classifier='"%s"' % self.classifier,
                    mmult='s' if len(self.duplicated_modifiers) > 1 else '',
                    modifiers=', '.join(self.duplicated_modifiers)))

    def _prefix(self):
        raise NotImplemented()


class FieldModifiersDuplication(MemberModifiersDuplication):
    def __init__(self, classifier, declaration):
        super(FieldModifiersDuplication, self).__init__(classifier, declaration)

    def _prefix(self):
        vars_decls = self.declaration.variable_declarators
        return ('Field variable{fmult} {vars} of'.format(
            fmult='s' if len(vars_decls) > 1 else '',
            vars=', '.join('"%s"' % v.variable.name for v in vars_decls)))


class MethodModifiersDuplication(MemberModifiersDuplication):
    def __init__(self, classifier, declaration):
        super(MethodModifiersDuplication, self).__init__(classifier,
                                                         declaration)

    def _prefix(self):
        return 'Method "%s" of' % self.declaration.name


class FormalParameterModifiersDuplication(MemberModifiersDuplication):
    def __init__(self, classifier, method, declaration):
        super(FormalParameterModifiersDuplication, self).__init__(
            classifier, declaration)
        self.method = method

    def _prefix(self):
        return ('Formal parameter {param} of method {method} in'.format(
            param='"%s"' % self.declaration.variable.name,
            method='"%s"' % self.method.name))


class PlyjDeclarationTypeError(Exception):
    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return 'Not a type of declaration: %s' % type(self.declaration)


class PlyjNameTypeError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Not a name of type: %s' % type(self.name)


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
            return 'Type name {type} used in {classifier} not found'.format(
                type='"%s"' % get_name_value(self.declaration.name),
                classifier='"%s"' % self.classifier.name)
        return 'Type name {type} not found'.format(
            type='"%s"' % get_name_value(self.declaration.name))


class AmbiguousTypeName(TypeNameError):
    def __init__(self, classifier, declaration, candidates):
        super(AmbiguousTypeName, self).__init__(classifier, declaration)
        self.candidates = candidates

    def __str__(self):
        from java_parser.full_classifiers_names import get_name_value
        if self.classifier:
            return ('Type name {type} used in {classifier} is ambiguous, '
                    'candidates is {candidates}').format(
                        type='"%s"' % get_name_value(self.declaration.name),
                        classifier='"%s"' % self.classifier.name,
                        candidates=self.__format_candidates())
        return ('Type name {type} is ambiguous, candidates is {'
                'candidates}'.format(
                    type='"%s"' % get_name_value(self.declaration.name),
                    candidates=self.__format_candidates()))

    def __format_candidates(self):
        return ', '.join('"%s"' % x for x in self.candidates)
