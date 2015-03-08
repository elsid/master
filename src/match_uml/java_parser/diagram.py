# coding: utf-8

from plyj.parser import Parser
from uml_matcher import Diagram, PrimitiveType
from java_parser import (
    set_full_classifiers_names, make_classifiers, make_external_classifiers,
    make_generalizations, set_full_types_names, fill_classifiers,
    make_associations)
from java_parser.external_classifiers import find_files
from java_parser.classifiers_members import PRIMITIVE_TYPES


def find_java_files(path):
    return (f for f in find_files(path) if f.endswith('.java'))


def parse_java_file(file_path):
    parser = Parser()
    return parser.parse_file(file_path)


class DiagramFactory(object):
    errors = None
    files = None
    trees = None
    classifiers = None
    generalizations = tuple()
    types = None
    associations = tuple()

    def __init__(self, dirs=None, files=None, trees=None,
                 external_path_list=None):
        self.dirs = list(dirs) if dirs else []
        self.files = list(files) if files else []
        self.trees = list(trees) if trees else []
        self.external_path_list = (list(external_path_list)
                                   if external_path_list else [])

    def product(self):
        self.errors = []
        self.__find_files()
        self.__parse_files()
        self.__set_full_classifiers_names()
        self.__make_classifiers()
        self.__make_primitive_types()
        if self.external_path_list:
            self.__make_external_classifiers()
        self.__set_full_types_names()
        self.__make_generalizations()
        self.__fill_classifiers()
        self.__make_associations()
        return Diagram(self.generalizations, self.associations)

    def __find_files(self):
        for dir_path in self.dirs:
            self.files += list(find_java_files(dir_path))

    def __parse_files(self):
        self.trees += [parse_java_file(path) for path in self.files]

    def __set_full_classifiers_names(self):
        for tree in self.trees:
            set_full_classifiers_names(tree)

    def __make_primitive_types(self):
        for name in PRIMITIVE_TYPES:
            self.classifiers[name] = PrimitiveType(name)

    def __make_classifiers(self):
        self.classifiers = {}
        for tree in self.trees:
            cur_classifiers, cur_errors = make_classifiers(tree)
            self.classifiers.update(cur_classifiers)
            self.errors += cur_errors

    def __make_external_classifiers(self):
        for tree in self.trees:
            cur_classifiers, cur_errors = make_external_classifiers(
                tree, self.external_path_list)
            self.classifiers.update(cur_classifiers)
            self.errors += cur_errors

    def __make_generalizations(self):
        self.generalizations = []
        for tree in self.trees:
            self.generalizations += make_generalizations(tree, self.classifiers)

    def __set_full_types_names(self):
        for tree in self.trees:
            self.errors += set_full_types_names(tree, self.classifiers)

    def __fill_classifiers(self):
        self.types = {}
        for tree in self.trees:
            cur_types, cur_errors = fill_classifiers(tree, self.classifiers)
            self.types.update(cur_types)
            self.errors += cur_errors

    def __make_associations(self):
        self.associations = make_associations(self.types)


def make_diagram(dirs=None, files=None, trees=None, external_path_list=None):
    factory = DiagramFactory(dirs, files, trees, external_path_list)
    diagram = factory.product()
    return diagram, factory.errors
