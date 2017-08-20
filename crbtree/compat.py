import functools

import six


def return_list_if_py2(method):
    if six.PY3:
        return method
    @functools.wraps(method)
    def list_method(self, *args, **kwargs):
        return list(method(self, *args, **kwargs))
    list_method._iterator = method
    return list_method


if six.PY3:
    izip = zip
else:
    import itertools
    izip = itertools.izip
