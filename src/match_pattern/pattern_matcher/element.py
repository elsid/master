# coding: utf-8

from pattern_matcher.cached_method import cached_method


class Element(object):
    @cached_method
    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return hash(self) < hash(other)

    def update(self, **kwargs):
        for attr, value in kwargs.iteritems():
            if hasattr(self, attr):
                setattr(self, attr, value)

    @staticmethod
    def _yaml_representer(dumper, value, **kwargs):
        tag = u'!%s' % value.__class__.__name__
        mapping = {k: v for k, v in kwargs.iteritems() if v is not None}
        return dumper.represent_mapping(tag, mapping)

    @classmethod
    def yaml_constructor(cls, loader, node):
        result = cls()
        yield result
        result.update(**loader.construct_mapping(node))
