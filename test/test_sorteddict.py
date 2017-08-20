import gc

from nose.tools import assert_equals
from nose.tools import assert_not_equals
from nose.tools import assert_raises

from crbtree import SortedDict


def test_smoke():
    sdict = SortedDict()
    assert_equals(len(sdict), 0)
    assert_equals(list(sdict), [])
    assert 'a' not in sdict
    assert 'b' not in sdict

    sdict['a'] = 123
    assert_equals(sdict['a'], 123)
    assert_equals(len(sdict), 1)
    assert 'a' in sdict
    assert_equals(list(sdict), ['a'])

    sdict['b'] = 456
    assert_equals(sdict['b'], 456)
    assert_equals(len(sdict), 2)
    assert 'b' in sdict
    assert_equals(list(sdict), ['a', 'b'])

    sdict['a'] = 789
    assert_equals(sdict['a'], 789)
    assert_equals(len(sdict), 2)
    assert 'a' in sdict
    assert 'b' in sdict
    assert_equals(list(sdict), ['a', 'b'])

    del sdict['b']
    assert_equals(len(sdict), 1)
    assert 'a' in sdict
    assert 'b' not in sdict
    assert_equals(list(sdict), ['a'])
    with assert_raises(KeyError):
        sdict['b']
    with assert_raises(KeyError):
        del sdict['b']
        del sdict['b']
        del sdict['b']


def test_initialize():
    sdict = SortedDict(a=123, b=456)
    assert_equals(len(sdict), 2)
    assert_equals(sdict['a'], 123)
    assert_equals(sdict['b'], 456)

    sdict = SortedDict([('a', 123), ('b', 456)])
    assert_equals(len(sdict), 2)
    assert_equals(sdict['a'], 123)
    assert_equals(sdict['b'], 456)

    sdict = SortedDict([('a', 123), ('b', 456)], c=789)
    assert_equals(len(sdict), 3)
    assert_equals(sdict['a'], 123)
    assert_equals(sdict['b'], 456)
    assert_equals(sdict['c'], 789)

    sdict = SortedDict({'a': 123, 'b': 456})
    assert_equals(len(sdict), 2)
    assert_equals(sdict['a'], 123)
    assert_equals(sdict['b'], 456)

    with assert_raises(TypeError):
        SortedDict('abc')

    with assert_raises(TypeError):
        SortedDict('key', 'value')

    with assert_raises(TypeError):
        SortedDict(123)


def test_equals():
    sdict1 = SortedDict(a=123, b=456)
    sdict2 = SortedDict(a=123, b=456)
    sdict3 = SortedDict(a=123, b=456, c=789)
    assert_equals(sdict1, sdict2)
    assert_not_equals(sdict1, sdict3)
    assert_not_equals(sdict2, sdict3)
    assert_not_equals(sdict3, {'a': 123, 'b': 456, 'c': 789})


def test_memory_management():
    sdict = SortedDict()
    assert_equals(len(sdict._handles), 0)
    sdict['a'] = 123
    assert_equals(len(sdict._handles), 1)
    del sdict['a']
    assert_equals(len(sdict._handles), 0)
    sdict['a'] = 456
    first_handles = list(sdict._handles)
    sdict['a'] = 789
    second_handles = list(sdict._handles)
    assert_not_equals(first_handles, second_handles)


def test_destructor():
    sdict = SortedDict()
    sdict['a'] = 123
    sdict.__del__()


def test_ordering_maintained():
    sdict = SortedDict()
    for i, char in enumerate('abcdefghijkl'):
        sdict[char] = i

    assert_equals(list(sdict), list('abcdefghijkl'))


def test_reversed():
    sdict = SortedDict(a=123, b=456, c=789)
    rsdict = reversed(sdict)
    rsdict2 = reversed(sdict)

    assert 'a' in rsdict
    assert_equals(rsdict['a'], 123)

    assert_equals(len(rsdict), len(sdict))
    assert_equals(list(rsdict), ['c', 'b', 'a'])
    assert_equals(list(rsdict.iterkeys()), ['c', 'b', 'a'])
    assert_equals(list(rsdict.itervalues()), [789, 456, 123])
    assert_equals(list(rsdict.iteritems()), [('c', 789), ('b', 456), ('a', 123)])

    assert_equals(rsdict.keys(), ['c', 'b', 'a'])
    assert_equals(rsdict.values(), [789, 456, 123])
    assert_equals(rsdict.items(), [('c', 789), ('b', 456), ('a', 123)])

    assert_not_equals(sdict, rsdict)
    assert_not_equals(rsdict, sdict)
    assert_not_equals(rsdict, None)
    assert_equals(rsdict, rsdict2)

    assert_equals(reversed(rsdict), sdict)
    assert_equals(sdict, reversed(rsdict))


def test_reversed_equal():
    sdict = SortedDict()
    rsdict = reversed(sdict)

    assert_equals(sdict, rsdict)
    assert_equals(rsdict, sdict)
