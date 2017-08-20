cRBTree
=======

A ``SortedDict`` and ``SortedSet`` implementation, backed by a
`red-black
tree <https://en.wikipedia.org/wiki/Red%E2%80%93black_tree>`__
implementation in C, wrapped with
`CFFI <https://cffi.readthedocs.org/>`__.

``SortedDict`` and ``SortedSet`` are collections that always iterate
through their keys/contents in order. Usage is simple:

::

    >>> sd = SortedDict()
    >>> sd['c'] = 789
    >>> sd['b'] = 456
    >>> sd['a'] = 123
    >>> for key, value in sd.iteritems():
    ...     print((key, value))
    ('a', 123)
    ('b', 456)
    ('c', 789)

You can iterate in reverse order by getting a reversed view of the
underlying ``SortedDict`` or ``Set``:

::

    >>> rsd = reversed(sd)
    >>> for key, value in sd.iteritems():
    ...     print((key, value))
    ('c', 789)
    ('b', 456)
    ('a', 123)

Installation
------------

::

    pip install crbtree

Unlicense
---------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of
this software dedicate any and all copyright interest in the software to
the public domain. We make this dedication for the benefit of the public
at large and to the detriment of our heirs and successors. We intend
this dedication to be an overt act of relinquishment in perpetuity of
all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org/
