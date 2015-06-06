# coding: utf-8

from os.path import dirname, realpath, join
from subprocess import check_output
from hamcrest import assert_that, equal_to

BASE_DIR = dirname(realpath(__file__))
DATA_DIR = join(BASE_DIR, 'data')
MODEL_DIR = join(DATA_DIR, 'model')
PATTERN_DIR = join(DATA_DIR, 'pattern')
MATCH_DIR = join(DATA_DIR, 'match')
MATCH_PATTERN_DIR = join(BASE_DIR, '../match_pattern')
PATTERN_MODEL = join(MATCH_PATTERN_DIR, 'pattern_model.py')
MATCH_PATTERN = join(MATCH_PATTERN_DIR, 'match_pattern.py')


def make_pattern_model(name):
    model = check_output(['python', PATTERN_MODEL, name])
    pattern_path = join(PATTERN_DIR, name + '.yaml')
    open(pattern_path, 'w').write(model)
    return pattern_path


def match_pattern(target, pattern, limit=None):
    command = ['python', MATCH_PATTERN]
    if limit:
        command += ['-l', str(limit)]
    return check_output(command + [target, pattern])


def load_match_result(name):
    return open(join(MATCH_DIR, name + '.log')).read()


def base_test_match_pattern(name, target_name, pattern_name, limit=None):
    pattern_path = make_pattern_model(pattern_name)
    target_path = join(MODEL_DIR, target_name + '.yaml')
    match_result = match_pattern(target_path, pattern_path, limit)
    assert_that(match_result, equal_to(load_match_result(name)))


def test_match_empty_in_empty():
    base_test_match_pattern('empty', 'empty', 'Empty')


def test_match_base_derived_in_extends():
    base_test_match_pattern('base_derived_in_extends', 'extends', 'BaseDerived')


def test_match_base_derived_in_implements():
    base_test_match_pattern('base_derived_in_implements', 'implements',
                            'BaseDerived')


def test_match_overridden_method_call_in_overridden_method_call():
    base_test_match_pattern('overridden_method_call', 'overridden_method_call',
                            'OverriddenMethodCall')


def test_match_all_base_derived_in_hierarchy():
    base_test_match_pattern('all_base_derived_in_hierarchy', 'hierarchy',
                            'BaseDerived')


def test_match_one_base_derived_in_hierarchy():
    base_test_match_pattern('one_base_derived_in_hierarchy', 'hierarchy',
                            'BaseDerived', 1)


def test_match_three_base_derived_in_hierarchy():
    base_test_match_pattern('three_base_derived_in_hierarchy', 'hierarchy',
                            'BaseDerived', 3)
