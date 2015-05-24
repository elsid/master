# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, calling, raises, empty
from plyj.model import (
    FieldDeclaration, MethodDeclaration, Name as PlyjName, Type as PlyjType,
    VariableDeclarator, Variable, ClassDeclaration)
from pattern_matcher import (
    Visibility, Type, Class, Property, Operation, Parameter, PrimitiveType,
    Enumeration, Direction)
from java_source_parser.classifiers import make_classifiers
from java_source_parser.classifiers_members import (
    get_visibility, has_duplications, get_name_value, format_type_arguments,
    get_type_name, get_classifier_name, VariableType, fill_classifiers,)
from java_source_parser.test.classifiers import TestCaseWithParser
from java_source_parser.errors import PlyjNameTypeError, ClassRedeclaration


class GetVisibility(TestCase):
    def test_get_from_public_field_should_be_public(self):
        assert_that(get_visibility(
            FieldDeclaration('int', [], modifiers=['public'])),
            equal_to(Visibility.PUBLIC))

    def test_get_from_public_method_should_be_public(self):
        assert_that(get_visibility(
            MethodDeclaration('', return_type='void', modifiers=['public'])),
            equal_to(Visibility.PUBLIC))

    def test_get_from_protected_field_should_be_protected(self):
        assert_that(get_visibility(
            FieldDeclaration('int', [], modifiers=['protected'])),
            equal_to(Visibility.PROTECTED))

    def test_get_from_private_field_should_be_private(self):
        assert_that(get_visibility(
            FieldDeclaration('int', [], modifiers=['private'])),
            equal_to(Visibility.PRIVATE))

    def test_get_from_field_without_visibility_should_be_private(self):
        assert_that(get_visibility(
            FieldDeclaration('int', [], modifiers=['private'])),
            equal_to(Visibility.PRIVATE))


class HasDuplications(TestCase):
    def test_empty_should_return_false(self):
        assert_that(has_duplications([]), equal_to(False))

    def test_with_one_should_return_false(self):
        assert_that(has_duplications([1]), equal_to(False))

    def test_many_different_should_return_false(self):
        assert_that(has_duplications([1, 2, 3]), equal_to(False))

    def test_two_same_should_return_true(self):
        assert_that(has_duplications([1, 1]), equal_to(True))

    def test_many_with_two_same_should_return_true(self):
        assert_that(has_duplications([1, 2, 3, 1]), equal_to(True))


class GetNameValue(TestCase):
    def test_get_from_str_should_succeed(self):
        assert_that(get_name_value('name'), equal_to('name'))

    def test_get_from_plyj_name_should_succeed(self):
        assert_that(get_name_value(PlyjName('name')), equal_to('name'))

    def test_get_from_int_should_return_error(self):
        assert_that(calling(lambda: get_name_value(42)),
                    raises(PlyjNameTypeError))


class FormatTypeArguments(TestCase):
    def test_format_empty_should_succeed(self):
        assert_that(format_type_arguments([]), equal_to(''))

    def test_format_one_should_succeed(self):
        assert_that(format_type_arguments(['int']), equal_to('<>'))

    def test_format_two_should_succeed(self):
        assert_that(format_type_arguments(['int', 'float']),
                    equal_to('<>'))


class GetTypeName(TestCase):
    def test_get_from_str_should_succeed(self):
        assert_that(get_type_name('int'), equal_to('int'))

    def test_get_from_plyj_type_should_succeed(self):
        assert_that(get_type_name(PlyjType('int')), equal_to('int'))

    def test_get_from_plyj_array_type_should_succeed(self):
        assert_that(get_type_name(PlyjType('int', dimensions=1)),
                    equal_to('int[]'))

    def test_get_from_plyj_type_with_add_dimensions_should_succeed(self):
        assert_that(get_type_name(PlyjType('int'), 1), equal_to('int[]'))

    def test_get_from_plyj_array_type_with_add_dimensions_should_succeed(self):
        assert_that(get_type_name(PlyjType('int', dimensions=1), 1),
                    equal_to('int[][]'))

    def test_get_from_template_plyj_type_should_succeed(self):
        assert_that(get_type_name(PlyjType('List', type_arguments=['int'])),
                    equal_to('List<>'))

    def test_get_from_template_with_two_args_should_succeed(self):
        assert_that(get_type_name(
            PlyjType('HashMap', type_arguments=['String', 'int'])),
            equal_to('HashMap<>'))

    def test_get_from_template_with_inserted_template_should_succeed(self):
        assert_that(get_type_name(
            PlyjType('HashMap',
                     type_arguments=['String',
                                     PlyjType('List',
                                              type_arguments=['int'])])),
                    equal_to('HashMap<>'))


class GetClassifierName(TestCase):
    def test_get_from_str_should_succeed(self):
        assert_that(get_classifier_name('int'), equal_to('int'))

    def test_get_from_plyj_type_should_succeed(self):
        assert_that(get_classifier_name(PlyjType('int')), equal_to('int'))

    def test_get_from_plyj_array_type_should_succeed(self):
        assert_that(get_classifier_name(PlyjType('int', dimensions=1)),
                    equal_to('int'))

    def test_get_from_template_with_inserted_template_should_succeed(self):
        assert_that(get_classifier_name(
            PlyjType('HashMap',
                     type_arguments=['String',
                                     PlyjType('List',
                                              type_arguments=['int'])])),
                    equal_to('HashMap'))


class MakeVariableType(TestCase):
    def test_make_primitive_should_succeed(self):
        variable_decl = VariableDeclarator(Variable(''))
        field = FieldDeclaration('int', [variable_decl])
        variable_type = VariableType(field, variable_decl.variable)
        assert_that(variable_type.type(None), equal_to(Type()))
        assert_that(variable_type.type_name(), equal_to('int'))
        assert_that(variable_type.classifier_name(), equal_to('int'))

    def test_make_array_should_succeed(self):
        variable_decl = VariableDeclarator(Variable('', dimensions=1))
        field = FieldDeclaration(PlyjType('A', dimensions=1), [variable_decl])
        variable_type = VariableType(field, variable_decl.variable)
        classifier = Class('A')
        assert_that(variable_type.type(classifier),
                    equal_to(Type(classifier, mult_lower=0, mult_upper=None)))
        assert_that(variable_type.type_name(), equal_to('A[][]'))
        assert_that(variable_type.classifier_name(), equal_to('A'))


VOID_TYPE = Type(PrimitiveType('void'))
INT_TYPE = Type(PrimitiveType('int'))
FLOAT_TYPE = Type(PrimitiveType('float'))


class FillClassifiers(TestCaseWithParser):
    def test_fill_empty_should_succeed(self):
        assert_that(fill_classifiers(self.parse(''), {}), equal_to(({}, [])))

    def test_fill_one_class_with_one_property_should_succeed(self):
        tree = self.parse('''
            class A {
                public int a;
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        assert_that(classifiers, equal_to({
            'A': Class('A', properties=[
                Property(INT_TYPE, 'a', Visibility.PUBLIC, is_static=False)
            ]),
            'int': INT_TYPE.classifier,
        }))

    def test_fill_one_class_with_two_same_property_should_return_error(self):
        tree = self.parse('''
            class A {
                public int a;
                public float a;
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(len(errors), equal_to(1))
        assert_that(str(errors[0]), equal_to(
            'error: redeclaration of variable "a" in class "A"'))
        assert_that(classifiers, equal_to({
            'A': Class('A', properties=[
                Property(INT_TYPE, 'a', Visibility.PUBLIC, is_static=False),
            ]),
            'int': INT_TYPE.classifier,
        }))

    def test_fill_one_class_with_one_operation_should_succeed(self):
        tree = self.parse('''
            class A {
                void f(int x);
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        assert_that(classifiers, equal_to({
            'A': Class('A', operations=[
                Operation('f', VOID_TYPE, Visibility.PRIVATE,
                          [Parameter('x', INT_TYPE, Direction.IN)],
                          is_static=False),
            ]),
            'void': VOID_TYPE.classifier,
            'int': INT_TYPE.classifier,
        }))

    def test_fill_one_class_with_two_overloaded_operations_should_succeed(self):
        tree = self.parse('''
            class A {
                void f(int x);
                void f(float x);
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        assert_that(classifiers, equal_to({
            'A': Class('A', operations=[
                Operation('f', VOID_TYPE, Visibility.PRIVATE,
                          [Parameter('x', INT_TYPE, Direction.IN)],
                          is_static=False),
                Operation('f', VOID_TYPE, Visibility.PRIVATE,
                          [Parameter('x', FLOAT_TYPE, Direction.IN)],
                          is_static=False),
            ]),
            'void': VOID_TYPE.classifier,
            'int': INT_TYPE.classifier,
            'float': FLOAT_TYPE.classifier,
        }))

    def test_fill_one_class_with_local_class_should_succeed(self):
        tree = self.parse('''
            class A {
                void f() {
                    class B extends A {
                        void g();
                    }
                }
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        assert_that(classifiers, equal_to({
            'A': Class('A', operations=[
                Operation('f', VOID_TYPE, Visibility.PRIVATE, is_static=False),
            ]),
            'B': Class('B', operations=[
                Operation('g', VOID_TYPE, Visibility.PRIVATE, is_static=False),
            ]),
            'void': VOID_TYPE.classifier,
        }))

    def test_fill_one_class_with_two_same_operations_should_return_error(self):
        tree = self.parse('''
            class A {
                void f(int x);
                void f(int x);
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(len(errors), equal_to(1))
        assert_that(str(errors[0]), equal_to(
            'error: redeclaration of method "-A::f(in x: int): void" in class '
            '"A"')
        )
        assert_that(classifiers, equal_to({
            'A': Class('A', operations=[
                Operation('f', VOID_TYPE, Visibility.PRIVATE,
                          [Parameter('x', INT_TYPE, Direction.IN)],
                          is_static=False),
            ]),
            'void': VOID_TYPE.classifier,
            'int': INT_TYPE.classifier,
        }))

    def test_fill_recursive_class_should_succeed(self):
        tree = self.parse('''
            class A {
                public A a;
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        a_type = Type(Class('A'))
        a_type.classifier.properties = [
            Property(a_type, 'a', Visibility.PUBLIC, is_static=False),
        ]
        assert_that(classifiers, equal_to({'A': a_type.classifier}))

    def test_fill_class_with_overriding_method_in_object_should_succeed(self):
        tree = self.parse('''
            class A {
                void g();
                void f() {
                    new A() {
                        public void h();
                    };
                }
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, empty())
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(errors, empty())
        assert_that(classifiers, equal_to({
            'A': Class('A', operations=[
                Operation('f', VOID_TYPE, Visibility.PRIVATE, is_static=False),
                Operation('g', VOID_TYPE, Visibility.PRIVATE, is_static=False),
            ]),
            'void': VOID_TYPE.classifier,
        }))

    def test_fill_two_same_sub_classes_should_return_error(self):
        tree = self.parse('''
            class Class {
                class SubClass {}
                class SubClass {}
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        assert_that(errors, equal_to(
            [ClassRedeclaration(ClassDeclaration('SubClass', []))]))
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(classifiers, equal_to({
            'Class': Class('Class'),
            'SubClass': Class('SubClass'),
        }))
        assert_that(errors, empty())

    def test_fill_enum_with_overriding_in_item_should_succeed(self):
        tree = self.parse('''
            enum Enum {
                Item {
                    @Override
                    public void f() {}
                };
                public abstract void f();
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        _, errors = fill_classifiers(tree, classifiers)
        assert_that(classifiers, equal_to({
            'Enum': Enumeration('Enum', operations=[
                Operation('f', VOID_TYPE, Visibility.PUBLIC, is_static=False),
            ]),
            'void': VOID_TYPE.classifier,
        }))
        assert_that(errors, empty())

    def test_fill_class_with_field_instance_creation_item_should_succeed(self):
        tree = self.parse('''
            class Class {
                Class value = new Class() {
                    @Override
                    public void f() {};
                };
                public abstract void f();
            }
        ''')
        classifiers, errors = make_classifiers(tree)
        _, errors = fill_classifiers(tree, classifiers)
        class_type = Type(Class('Class', operations=[
            Operation('f', VOID_TYPE, Visibility.PUBLIC, is_static=False),
        ]))
        class_type.classifier.properties = [
            Property(class_type, 'value', Visibility.PRIVATE, is_static=False)]
        assert_that(classifiers, equal_to({
            'Class': class_type.classifier,
            'void': VOID_TYPE.classifier,
        }))
        assert_that(errors, empty())

if __name__ == '__main__':
    main()
