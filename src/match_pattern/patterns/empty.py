# coding: utf-8

from utils import cached_method
from pattern_matcher import Model


class Empty(object):
    @cached_method
    def create(self):
        return Model()


if __name__ == '__main__':
    print Empty().create()
