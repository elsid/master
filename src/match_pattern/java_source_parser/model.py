# coding: utf-8

from os.path import isdir, isfile
from plyj.parser import Parser
from pattern_matcher import Model
from java_source_parser import (
    set_full_classifiers_names, make_classifiers, make_external_classifiers,
    make_generalizations, set_full_types_names, fill_classifiers,
    make_dependencies)
from java_source_parser.external_classifiers import find_files

from java_source_parser.errors import InvalidPath, PlyjSyntaxError


def find_java_files(path):
    return (f for f in find_files(path) if f.endswith('.java'))


class ModelFactory(object):
    errors = None
    trees = None
    classifiers = None
    types = None

    def __init__(self, path_list=None, trees=None, external_path_list=None):
        self.path_list = list(path_list) if path_list else []
        self.files = []
        self.trees = list(trees) if trees else []
        self.external_path_list = (list(external_path_list)
                                   if external_path_list else [])

    def product(self):
        self.errors = []
        self.__find_files()
        self.__parse_files()
        self.__set_full_classifiers_names()
        self.__make_classifiers()
        if self.external_path_list:
            self.__make_external_classifiers()
        self.__set_full_types_names()
        self.__make_generalizations()
        self.__fill_classifiers()
        self.__make_dependencies()
        return Model(t.classifier for t in self.types.itervalues())

    def __find_files(self):
        for path in self.path_list:
            if isdir(path):
                self.files += list(find_java_files(path))
            elif isfile(path):
                self.files.append(path)
            else:
                raise InvalidPath(path)

    def __parse_file(self, file_path):
        parser = Parser()
        tree = parser.parse_file(file_path)
        self.errors += [PlyjSyntaxError(file_path, e) for e in parser.errors()]
        return tree

    def __parse_files(self):
        parse = self.__parse_file
        self.trees += [t for t in (parse(f) for f in self.files) if t]

    def __set_full_classifiers_names(self):
        for tree in self.trees:
            set_full_classifiers_names(tree)

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
        for tree in self.trees:
            make_generalizations(tree, self.classifiers)

    def __set_full_types_names(self):
        for tree in self.trees:
            self.errors += set_full_types_names(tree, self.classifiers)

    def __fill_classifiers(self):
        self.types = {}
        for tree in self.trees:
            cur_types, cur_errors = fill_classifiers(tree, self.classifiers)
            self.types.update(cur_types)
            self.errors += cur_errors

    def __make_dependencies(self):
        for tree in self.trees:
            make_dependencies(tree, self.types)


def make_model(path_list=None, trees=None, external_path_list=None):
    factory = ModelFactory(path_list, trees, external_path_list)
    model = factory.product()
    return model, factory.errors
