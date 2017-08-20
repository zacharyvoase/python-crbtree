from nose.tools import assert_equals
from nose.tools import assert_not_equals
from nose.tools import assert_raises

from crbtree import SortedSet


def test_smoke():
    sset = SortedSet()
    assert_equals(len(sset), 0)
    assert_equals(list(sset), [])

    sset.add('a')
    assert_equals(len(sset), 1)
    assert_equals(list(sset), ['a'])

    sset.add('b')
    assert_equals(len(sset), 2)
    assert_equals(list(sset), ['a', 'b'])

    sset.discard('a')
    assert_equals(len(sset), 1)
    assert_equals(list(sset), ['b'])


def test_initialize():
    sset = SortedSet('abcdefghijkl')
    assert_equals(len(sset), len('abcdefghijkl'))
    assert_equals(list(sset), list('abcdefghijkl'))


def test_equals():
    sset1 = SortedSet('abc')
    sset2 = SortedSet('abc')
    sset3 = SortedSet('abcd')
    assert_equals(sset1, sset2)
    assert_not_equals(sset1, sset3)
    assert_not_equals(sset2, sset3)
    sset2.add('d')
    assert_not_equals(sset1, sset2)
    assert_equals(sset2, sset3)


def test_reversed():
    sset = SortedSet(['a', 'b', 'c'])
    assert_equals(list(reversed(sset)), ['c', 'b', 'a'])
