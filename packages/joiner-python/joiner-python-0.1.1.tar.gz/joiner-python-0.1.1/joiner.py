# -*- coding: utf-8 -*-
from weakref import WeakKeyDictionary
from itertools import product

__version__ = '0.1.1'

_DATA = WeakKeyDictionary()
_INDEXES = WeakKeyDictionary()
_FORMATTERS = WeakKeyDictionary()


class Dict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def _hashable(x):
    try:
        hash(x)
        return True
    except TypeError:
        return False


def _none(values):
    return any(value is None for value in values)


def _indexable(values):
    if _none(values):
        return False
    return all(_hashable(value) for value in values)


def _formatter_of(group):
    return _FORMATTERS[group]


class Cols(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    @property
    def mappings(self):
        ret = [(arg, arg) for arg in self._args]
        ret.extend(self._kwargs.items())
        return ret


class Group(object):

    def __init__(self, rows, cols=None, defaults=None):
        _DATA[self] = list(rows)
        if isinstance(cols, (tuple, list, set)):
            cols = Cols(*cols)
            mappings = cols.mappings
        elif isinstance(cols, Cols):
            mappings = cols.mappings
        else:
            assert cols is None, 'Unexpected type: %s' % type(cols)
            mappings = None
        mappings = cols.mappings if isinstance(cols, Cols) else None

        def formatter(row):
            row = {} if row is None else row
            if mappings is None:
                if defaults:
                    temp = {}
                    for k, v in defaults.items():
                        if row.get(k) is None:
                            temp[k] = v
                    if temp:
                        row = dict(row)
                        row.update(temp)
                return row
            else:
                ret = {}
                for old_key, new_key in mappings:
                    value = row.get(old_key)
                    if value is None and defaults:
                        value = defaults.get(old_key)
                    ret[new_key] = value
                return ret

        _FORMATTERS[self] = formatter

    def __getattr__(self, attr):
        return GroupAttr(self, attr)

    def __iter__(self):
        for row in selectfrom(self).get():
            yield row


INNER_JOIN = 1
LEFT_JOIN = 2
RIGHT_JOIN = 3


class _Row(object):
    __slots__ = ('groups', 'data')

    def __init__(self, groups, data):
        self.groups = groups
        self.data = data

    def _value(self, attr):
        group, attr = attr.group, attr.attr
        index = self.groups.index(group)
        col = self.data[index]
        if col is None:
            return
        return col.get(attr)

    def get_values(self, attrs):
        return tuple(self._value(attr) for attr in attrs)

    def merge(self):
        ret = Dict()
        for group, col in zip(self.groups, self.data):
            col = _formatter_of(group)(col)
            for k, v in col.items():
                if k in ret:
                    assert v == ret[k], 'key "%s" conflicts: %s != %s' % (k, ret[k], v)
                    continue
                ret[k] = v
        return ret


class _Rows(object):
    def __init__(self, groups, datas):
        self.groups = groups
        self.datas = datas

    def get_datas(self, attrs, values):
        assert _indexable(values), '%s not indexable' % str(values)
        indexes = self._indexes_of(attrs)
        return indexes.get(values, [])

    def _indexes_of(self, attrs):
        key = tuple((attr.group, attr.attr) for attr in attrs)
        indexes = _INDEXES.get(self, {}).get(key)
        if indexes is None:
            indexes = _INDEXES.setdefault(self, {}).setdefault(key, {})
            for row in self:
                values = row.get_values(attrs)
                if _indexable(values):
                    indexes.setdefault(values, []).append(row.data)
        return indexes

    def __iter__(self):
        for data in self.datas:
            yield _Row(self.groups, data)


class _On(object):
    def __init__(self, *pairs):
        assert all(isinstance(pair, _Pair) for pair in pairs)
        self.pairs = pairs

    def join(self, left_rows, right_rows, mode=LEFT_JOIN):
        assert mode in (LEFT_JOIN, RIGHT_JOIN, INNER_JOIN), 'Invalid mode: %s' % mode
        if mode in (LEFT_JOIN, INNER_JOIN):
            left_rows, right_rows = left_rows, right_rows
        elif mode == RIGHT_JOIN:
            right_rows, left_rows = left_rows, right_rows

        lattrs, rattrs = zip(*(pair.split(left_rows, right_rows) for pair in self.pairs))

        def y():
            for _left_row in left_rows:
                values = _left_row.get_values(lattrs)
                if _none(values):
                    if mode != INNER_JOIN:
                        _left = _left_row.data
                        yield _left + (None,)
                else:
                    _left = _left_row.data
                    _rights = right_rows.get_datas(rattrs, values)
                    if _rights:
                        for _left, _right in product([_left], _rights):
                            yield _left + _right
                    elif mode != INNER_JOIN:
                        yield _left + (None,)

        return _Rows(left_rows.groups + right_rows.groups, y())


class GroupAttr(object):
    def __init__(self, group, attr):
        self.group = group
        self.attr = attr

    def __eq__(self, other):
        if not isinstance(other, GroupAttr):
            return NotImplemented
        return _Pair(self, other)


class _Pair(object):
    def __init__(self, L, R):
        self._L = L
        self._R = R

    def split(self, left_rows, right_rows):
        L, R = self._L, self._R
        lgroup, rgroup = L.group, R.group
        lgroups, rgroups = left_rows.groups, right_rows.groups
        if lgroup in lgroups:
            assert rgroup in rgroups
            return L, R
        assert lgroup in rgroups
        assert rgroup in lgroups
        return R, L


def _to_rows(x):
    assert isinstance(x, Group)

    def y():
        for each in _DATA[x]:
            yield (each,)
    return _Rows([x], y())


class Select(object):

    def __init__(self, group):
        self._left = _to_rows(group)
        self._right = None
        self._cur_mode = None

    def _join(self, group, mode):
        assert self._right is None
        assert self._cur_mode is None
        self._right = _to_rows(group)
        self._cur_mode = mode
        return self

    def leftjoin(self, group):
        return self._join(group, mode=LEFT_JOIN)

    def rightjoin(self, group):
        return self._join(group, mode=RIGHT_JOIN)

    def innerjoin(self, group):
        return self._join(group, mode=INNER_JOIN)

    def on(self, *pairs):
        on = _On(*pairs)
        assert self._right is not None
        assert self._cur_mode is not None
        try:
            self._left = on.join(self._left, self._right, mode=self._cur_mode)
        finally:
            self._right = None
            self._cur_mode = None
        return self

    def get(self, merge=True):
        if merge:
            for row in self._left:
                yield row.merge()
        else:
            for row in self._left:
                yield row


def select(group):
    return Select(group)


selectfrom = select

if __name__ == '__main__':
    def test():
        hobbys = [
            {'first_name': 'A', 'last_name': 'yao', 'hobby': 'pingpong'},
            {'first_name': 'A', 'last_name': 'bob', 'hobby': 'shopping'},
            {'first_name': 'B', 'last_name': 'bob', 'hobby': 'shopping'},
        ]
        ages = [
            {'first_name': 'A', 'last_name': 'yao', 'age': 18},
            {'first_name': 'A', 'last_name': 'bob', 'age': 20},
        ]
        heights = [
            {'first_name': 'A', 'last_name': 'yao', 'height': 170},
        ]

        hobbys = Group(hobbys)
        ages = Group(ages, cols=Cols('age', age='how old'))
        heights = Group(heights, cols=Cols('height'))
        results = selectfrom(hobbys).leftjoin(ages).on(hobbys.first_name == ages.first_name, hobbys.last_name == ages.last_name)\
            .leftjoin(heights).on(hobbys.first_name == heights.first_name, hobbys.last_name == heights.last_name)\
            .get()
        for result in results:
            print(result)

    test()
