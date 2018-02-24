# coding: utf-8


def cached_method(method):

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '__cache'):
            setattr(self, '__cache', {})
        cache = getattr(self, '__cache')
        if method in cache:
            return cache[method]
        result = method(self, *args, **kwargs)
        cache[method] = result
        return result

    return wrapper
