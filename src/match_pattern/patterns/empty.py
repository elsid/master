# coding: utf-8

from pattern_matcher import Model, cached_method


class Empty(object):
    @cached_method
    def create(self):
        return Model()


if __name__ == '__main__':
    print Empty().create()
