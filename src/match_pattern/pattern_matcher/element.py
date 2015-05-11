# coding: utf-8

from pattern_matcher.cached_method import cached_method


class Element(object):
    @cached_method
    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return hash(self) < hash(other)

    @staticmethod
    def _yaml_representer(dumper, value, **kwargs):
        tag = u'!%s' % value.__class__.__name__
        mapping = {k: v for k, v in kwargs.iteritems() if v is not None}
        return dumper.represent_mapping(tag, mapping)
