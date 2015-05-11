# coding: utf-8

from os import walk
from os.path import join, isdir, isfile
from plyj.model import Visitor
from javatools import unpack_classfile
from javatools.jarinfo import JarInfo
from pattern_matcher import Class, Interface, Enumeration
from java_parser.full_classifiers_names import get_name_value


def generate_subpaths(import_name):
    import_path = get_name_value(import_name).split('.')
    import_path_len = len(import_path)
    for begin in range(import_path_len + 1):
        subimport = import_path[begin:]
        for border in range(import_path_len - begin):
            subpackages = '/'.join(subimport[:border])
            subclasses = '$'.join(subimport[border:])
            yield (join(subpackages, subclasses)
                   if subpackages and subclasses else subpackages + subclasses)


def find_files(path):
    for root, _, files in walk(path):
        for file_path in files:
            yield join(root, file_path)


def make_class(class_info):
    return Class(class_info.pretty_this())


def make_interface(class_info):
    return Interface(class_info.pretty_this())


def make_enumeration(class_info):
    return Enumeration(class_info.pretty_this())


def make_classifier(class_info):
    if class_info.is_interface():
        return make_interface(class_info)
    elif class_info.is_enum():
        return make_enumeration(class_info)
    else:
        return make_class(class_info)


class JarFileCache(object):
    def __init__(self, jar_info):
        self.__jar_info = jar_info
        self.__class_files = {path: None for path in jar_info.get_classes()}

    def get(self, import_name):
        path = import_name.replace('.', '/')
        for class_file, class_info in self.__class_files.iteritems():
            if path in class_file:
                if not class_info:
                    class_info = self.__jar_info.get_classinfo(class_file)
                    self.__class_files[class_file] = class_info
                if import_name in class_info.pretty_this():
                    yield class_info


class ClassInfoCache(object):
    def __init__(self, path_list):
        self.__class_files = {}
        self.__jar_files = {}
        for path in path_list:
            if isdir(path):
                for file_path in find_files(path):
                    self.__process_file(file_path)
            elif isfile(path):
                self.__process_file(path)

    def get(self, import_name):
        for class_info in self.__get_from_class_files(import_name):
            yield class_info
        for class_info in self.__get_from_jar_files(import_name):
            yield class_info

    def __process_file(self, file_path):
        if file_path.endswith('.class'):
            self.__class_files[file_path] = None
        elif file_path.endswith('.jar'):
            jar_info = JarInfo(file_path)
            self.__jar_files[file_path] = JarFileCache(jar_info)

    def __get_from_class_files(self, import_name):
        for subpath in generate_subpaths(import_name):
            for class_info in self.__get_from_class_file(import_name, subpath):
                yield class_info

    def __get_from_class_file(self, import_name, subpath):
        for file_path, class_info in self.__class_files.iteritems():
            if subpath in file_path:
                if not class_info:
                    class_info = unpack_classfile(file_path)
                    self.__class_files[file_path] = class_info
                if import_name in class_info.pretty_this():
                    yield class_info

    def __get_from_jar_files(self, import_name):
        for jar_file_path, jar_file in self.__jar_files.iteritems():
            for class_info in jar_file.get(import_name):
                yield class_info


__class_info_cache = []


def get_class_info_cache(path_list):
    for cache_path_list, cache in __class_info_cache:
        if path_list == cache_path_list:
            return cache
    cache = ClassInfoCache(path_list)
    __class_info_cache.append((path_list, cache))
    return cache


FORCE_IMPORT = frozenset(['java.lang'])


class ExternalClassifiersFactory(Visitor):
    def __init__(self, path_list):
        super(ExternalClassifiersFactory, self).__init__()
        self.classifiers = {}
        self.errors = []
        self.__class_info_cache = get_class_info_cache(path_list)
        for import_name in FORCE_IMPORT:
            self.__add_import(import_name)

    def visit_ImportDeclaration(self, declaration):
        self.__add_import(get_name_value(declaration.name))

    def __add_import(self, import_name):
        for class_info in self.__class_info_cache.get(import_name):
            classifier = make_classifier(class_info)
            self.classifiers[classifier.name] = classifier


def make_external_classifiers(tree, paths):
    factory = ExternalClassifiersFactory(paths)
    tree.accept(factory)
    return factory.classifiers, factory.errors
