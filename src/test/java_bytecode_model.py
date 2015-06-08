# coding: utf-8

import pytest

from os import remove, makedirs, listdir
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


def make_model_from_source(file_name):
    source_path = join(SOURCE_DIR, file_name)
    target_dir = join(TARGET_DIR, file_name.replace('.java', ''))
    if exists(target_dir):
        if isdir(target_dir):
            rmtree(target_dir)
        else:
            remove(target_dir)
    makedirs(target_dir)
    compile_source(source_path, target_dir)
    return make_model(target_dir)


def load_model(file_name):
    return open(join(MODEL_DIR, file_name)).read()


FILES_NAMES = (x for x in listdir(SOURCE_DIR) if x.endswith('.java'))


@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_one_file(file_name):
    assert_that(make_model_from_source(file_name),
                equal_to(load_model(file_name.replace('.java', '.yaml'))))
