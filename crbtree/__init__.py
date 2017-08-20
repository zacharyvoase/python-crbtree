"""
A Dict and Set implementation which always iterate in order.

`SortedDict` and `SortedSet` are red-black tree-based collections, which store
their keys according to their native Python sort order. This means iteration
(i.e. `for key in dictionary:`, or `for value in set:`) always produces the
keys in order.
"""

import collections
import itertools

from crbtree._rbtree import ffi, lib


__all__ = ['SortedDict', 'SortedSet']


Item = collections.namedtuple('Item', ('key', 'value'))


class SortedDict(collections.MutableMapping):

    "A sorted dictionary, backed by a red-black tree."

    def __init__(self, *args, **kwargs):
        self._rbtree = lib.rb_tree_create(lib.rb_tree_node_compare)
        # This allows us to get the SortedDict Python object from a node
        # removal/dealloc callback.
        self._self_handle = ffi.new_handle(self)
        self._rbtree.info = self._self_handle
        # Track the FFI pointers to Items so they don't get garbage collected.
        self._handles = set()
        if args:
            if len(args) != 1:
                raise TypeError("SortedDict() expected exactly 0 or 1 positional args, got {}"
                                .format(len(args)))
            if isinstance(args[0], collections.Mapping):
                self.update(args[0])
            elif isinstance(args[0], collections.Iterable):
                for item in args[0]:
                    try:
                        key, value = item
                    except ValueError:
                        raise TypeError("SortedDict expected (key, value) pair, got {!r}".format(item))
                    self[key] = value
            else:
                raise TypeError("Cannot initialize SortedDict from {!r}".format(args[0]))
        if kwargs:
            self.update(kwargs)

    def __del__(self):
        lib.rb_tree_dealloc(self._rbtree, ffi.addressof(lib, 'rb_tree_node_dealloc_cb'))

    def __len__(self):
        return lib.rb_tree_size(self._rbtree)

    def _get(self, key):
        item = Item(key, None)
        item_p = ffi.new_handle(item)
        result_p = lib.rb_tree_find(self._rbtree, item_p)
        if result_p == ffi.NULL:
            return (False, None)
        return (True, ffi.from_handle(result_p).value)

    def __contains__(self, key):
        return self._get(key)[0]

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        item = Item(key, value)
        item_p = ffi.new_handle(item)
        self._handles.add(item_p)
        if not lib.rb_tree_insert(self._rbtree, item_p):
            raise RuntimeError("Unexpected error inserting key {!r}".format(key))

    def __getitem__(self, key):
        found, item = self._get(key)
        if found:
            return item
        raise KeyError(key)

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        item = Item(key, None)
        item_p = ffi.new_handle(item)
        removed = lib.rb_tree_remove_with_cb(self._rbtree, item_p, lib.rb_tree_node_was_removed)
        if not removed:
            raise RuntimeError("Unexpected error removing key {!r}".format(key))

    def __iter__(self):
        for key, value in self.iteritems():
            yield key

    def __eq__(self, other):
        if isinstance(other, ReversedSortedDictView):
            return len(self) < 2 and len(self) == len(other) and sorted_mapping_eq(self, other)
        elif not isinstance(other, SortedDict):
            return False
        return len(self) == len(other) and sorted_mapping_eq(self, other)

    def __reversed__(self):
        return ReversedSortedDictView(self)

    def iteritems(self):
        rb_iter = lib.rb_iter_create()
        try:
            item_p = lib.rb_iter_first(rb_iter, self._rbtree)
            while item_p != ffi.NULL:
                item = ffi.from_handle(item_p)
                yield (item.key, item.value)
                item_p = lib.rb_iter_next(rb_iter)
        finally:
            lib.rb_iter_dealloc(rb_iter)

    def reverse_iteritems(self):
        rb_iter = lib.rb_iter_create()
        try:
            item_p = lib.rb_iter_last(rb_iter, self._rbtree)
            while item_p != ffi.NULL:
                item = ffi.from_handle(item_p)
                yield (item.key, item.value)
                item_p = lib.rb_iter_prev(rb_iter)
        finally:
            lib.rb_iter_dealloc(rb_iter)

    def reverse_iterkeys(self):
        for key, value in self.reverse_iteritems():
            yield key

    def reverse_itervalues(self):
        for key, value in self.reverse_iteritems():
            yield value


class ReversedSortedDictView(object):
    __slots__ = ('sorted_dict',)

    def __init__(self, sorted_dict):
        self.sorted_dict = sorted_dict

    def __len__(self):
        return len(self.sorted_dict)

    def __contains__(self, key):
        return key in self.sorted_dict

    def __getitem__(self, key):
        return self.sorted_dict[key]

    def __iter__(self):
        return self.sorted_dict.reverse_iterkeys()

    def __eq__(self, other):
        if isinstance(other, ReversedSortedDictView):
            return self.sorted_dict == other.sorted_dict
        elif isinstance(other, SortedDict):
            return len(self) < 2 and len(self) == len(other) and sorted_mapping_eq(self, other)
        return False

    def __reversed__(self):
        return self.sorted_dict

    def iteritems(self):
        return self.sorted_dict.reverse_iteritems()

    def iterkeys(self):
        return iter(self)

    def itervalues(self):
        return self.sorted_dict.reverse_itervalues()

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())


class SortedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        if iterable is not None:
            self._dict = SortedDict((value, None) for value in iterable)
        else:
            self._dict = SortedDict()

    def __contains__(self, value):
        return value in self._dict

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return self._dict.iterkeys()

    def __reversed__(self):
        return self._dict.reverse_iterkeys()

    def add(self, value):
        self._dict.setdefault(value, None)

    def discard(self, value):
        self._dict.pop(value, None)


@ffi.def_extern()
def rb_tree_node_compare(rb_tree_p, rb_node_a, rb_node_b):
    a, b = ffi.from_handle(rb_node_a.value), ffi.from_handle(rb_node_b.value)
    if a.key == b.key:
        return 0
    if a.key < b.key:
        return -1
    return 1


@ffi.def_extern()
def rb_tree_node_was_removed(rb_tree_p, rb_node_p):
    ffi.from_handle(rb_tree_p.info)._handles.discard(rb_node_p.value)
    lib.rb_tree_node_dealloc_cb(rb_tree_p, rb_node_p)


def sorted_mapping_eq(map1, map2):
    return all(
        k1 == k2 and v1 == v2
        for (k1, v1), (k2, v2)
        in itertools.izip(map1.iteritems(), map2.iteritems()))
