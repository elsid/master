# coding: utf-8


def cached_eq(method):
    cache_name = '__%s_cache' % method.__name__

    def wrapper(self, other, *args, **kwargs):
        other_key = id(other)
        if not hasattr(self, cache_name):
            setattr(self, cache_name, {})
        method_cache = getattr(self, cache_name)
        if other_key in method_cache:
            return method_cache[other_key]
        method_cache[other_key] = True
        result = method(self, other, *args, **kwargs)
        method_cache[other_key] = result
        return result

    return wrapper
