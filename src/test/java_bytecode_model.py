# coding: utf-8

from os import remove, makedirs
from os.path import dirname, realpath, join, isdir, exists
from shutil import rmtree
from subprocess import check_call, check_output
from hamcrest import assert_that, equal_to

BASE_DIR = dirname(realpath(__file__))
SOURCE_DIR = join(BASE_DIR, 'data/src')
TARGET_DIR = join(BASE_DIR, 'data/target')
MODEL_DIR = join(BASE_DIR, 'data/model')
JAR = join(BASE_DIR, '../java_bytecode_model/target/'
                     'java_bytecode_model-1.0-SNAPSHOT.jar')


def compile_source(file_path, target_dir):
    return check_call(['javac', '-d', target_dir, file_path])


def make_model(target_path):
    return check_output(['java', '-jar', JAR, target_path])


def make_model_from_source(name):
    source_path = join(SOURCE_DIR, name + '.java')
    target_dir = join(TARGET_DIR, name)
    if exists(target_dir):
        if isdir(target_dir):
            rmtree(target_dir)
        else:
            remove(target_dir)
    makedirs(target_dir)
    compile_source(source_path, target_dir)
    return make_model(target_dir)


def load_model(name):
    return open(join(MODEL_DIR, name + '.yaml')).read()


def base_test_make_model(name):
    assert_that(make_model_from_source(name), equal_to(load_model(name)))


def test_make_empty_model():
    base_test_make_model('empty')


def test_make_class_model():
    base_test_make_model('class')


def test_make_base_derived_model():
    base_test_make_model('base_derived')


def test_make_overridden_method_call_model():
    base_test_make_model('overridden_method_call')


def test_make_hierarchy_model():
    base_test_make_model('hierarchy')
