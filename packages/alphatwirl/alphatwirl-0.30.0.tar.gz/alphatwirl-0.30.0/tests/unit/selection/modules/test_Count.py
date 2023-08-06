# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules.Count import Count

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return Count()

@pytest.fixture()
def sel1():
    ret= mock.Mock()
    ret.name ='sel1'
    ret.__class__.__name__ = 'MockEventSelection'
    return ret

@pytest.fixture()
def sel2():
    ret= mock.Mock()
    ret.name ='sel2'
    ret.__class__.__name__ = 'MockEventSelection'
    return ret

@pytest.fixture()
def sel3():
    ret= mock.Mock()
    ret.name = '' # empty string
    ret.__class__.__name__ = 'MockEventSelection'
    return ret

##__________________________________________________________________||
def test_add(sel1, sel2, sel3):
    obj = Count()
    assert 0 == len(obj._results)

    obj = Count(selections=[sel1, sel2])
    assert 2 == len(obj._results)
    obj.add(sel3)
    assert 3 == len(obj._results)

def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
def test_copy(obj):
    obj._results[:] = [[1, 'class', 'name', 2, 3]]
    obj1 = obj.copy()
    assert obj is not obj1
    assert obj._results is not obj1._results
    assert [[1, 'class', 'name', 2, 3]] == obj1._results

def test_increment_depth(obj):
    obj._results[:] = [
        [1, 'class1', 'name1', 6, 8],
        [1, 'class1', 'name2', 3, 6],
        [1, 'class2', 'name3', 1, 3],
    ]

    obj.increment_depth(by=1)

    assert [
        [2, 'class1', 'name1', 6, 8],
        [2, 'class1', 'name2', 3, 6],
        [2, 'class2', 'name3', 1, 3],
    ] == obj._results

def test_insert(obj):
    obj._results[:] = [
        [1, 'class1', 'name1', 6, 8],
        [1, 'class1', 'name2', 3, 6],
        [1, 'class2', 'name3', 1, 3],
    ]

    obj1 = Count()
    obj1._results[:] = [
        [2, 'class2', 'name4', 4, 6],
        [2, 'class3', 'name5', 3, 4],
    ]

    obj.insert(1, obj1)

    assert [
        [1, 'class1', 'name1', 6, 8],
        [1, 'class1', 'name2', 3, 6],
        [2, 'class2', 'name4', 4, 6],
        [2, 'class3', 'name5', 3, 4],
        [1, 'class2', 'name3', 1, 3],
    ] == obj._results

def test_insert_at_end(obj):

    obj._results[:] = [
        [1, 'class1', 'name1', 6, 8],
        [1, 'class1', 'name2', 3, 6],
        [1, 'class2', 'name3', 1, 3],
    ]

    obj1 = Count()
    obj1._results[:] = [
        [2, 'class2', 'name4', 2, 3],
        [2, 'class3', 'name5', 1, 2],
    ]

    obj.insert(2, obj1)

    assert [
        [1, 'class1', 'name1', 6, 8],
        [1, 'class1', 'name2', 3, 6],
        [1, 'class2', 'name3', 1, 3],
        [2, 'class2', 'name4', 2, 3],
        [2, 'class3', 'name5', 1, 2],
    ] == obj._results

##__________________________________________________________________||
def test_empty(obj):
    obj.count(pass_=[ ])

def test_one(obj, sel1):
    obj.add(sel1)

    assert [
        [1, 'MockEventSelection', 'sel1', 0, 0],
    ] == obj._results

    obj.count(pass_=[True])
    assert [
        [1, 'MockEventSelection', 'sel1', 1, 1],
    ] == obj._results

    obj.count(pass_=[False])
    assert [
        [1, 'MockEventSelection', 'sel1', 1, 2],
    ] == obj._results

def test_three(obj, sel1, sel2, sel3):
    obj.add(sel1)
    obj.add(sel2)
    obj.add(sel3)

    assert [
        [1, 'MockEventSelection', 'sel1', 0, 0],
        [1, 'MockEventSelection', 'sel2', 0, 0],
        [1, 'MockEventSelection',     '', 0, 0],
    ] == obj._results

    obj.count(pass_= [True, False])
    assert [
        [1, 'MockEventSelection', 'sel1', 1, 1],
        [1, 'MockEventSelection', 'sel2', 0, 1],
        [1, 'MockEventSelection',     '', 0, 0],
    ] == obj._results

    obj.count(pass_=[True, True, False])
    assert [
        [1, 'MockEventSelection', 'sel1', 2, 2],
        [1, 'MockEventSelection', 'sel2', 1, 2],
        [1, 'MockEventSelection',     '', 0, 1],
    ] == obj._results

def test_to_tuple_list(obj):
    obj._results[:] = [
        [1, 'class1', 'name1', 6, 8],
        [1, 'class1', 'name2', 3, 6],
        [1, 'class2', 'name3', 1, 3],
    ]
    assert [
        (1, 'class1', 'name1', 6, 8),
        (1, 'class1', 'name2', 3, 6),
        (1, 'class2', 'name3', 1, 3)
    ] == obj.to_tuple_list()

##__________________________________________________________________||
