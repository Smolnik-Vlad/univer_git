import pytest

from another_operations import Another_operations
from constants import Constants
from sets_and_operations import Sets_and_operations


def test_ordinary_set():
    assert Sets_and_operations().solution("{a, b, {c, d, {e, f}, g, {h, i}, j}}").from_class_to_set() == {'a', 'b',
                                                                                                          frozenset(
                                                                                                              {'c', 'd',
                                                                                                               'g', 'j',
                                                                                                               frozenset(
                                                                                                                   {'e',
                                                                                                                    'f'}),
                                                                                                               frozenset(
                                                                                                                   {'h',
                                                                                                                    'i'})})}
    assert Sets_and_operations().solution(
        "{a, b, {c}, {d, f}} * ({a, b, {g}} + {{d, f}} / {a})").from_class_to_set() == {'b', frozenset({'d', 'f'})}


def test_saved_set():
    a = Constants()
    b = Constants()
    res = Constants()
    a.read_line('A = {a, b, {c}, {d, e, {f}}}')
    b.read_line('B = {a, {d, e, {f}}}')
    res.read_line('{{c}}*(A - B)')
    assert a.my_set.from_class_to_set() == {'a', 'b', frozenset({'c'}), frozenset({'d', 'e', frozenset({'f',})})}
    assert b.my_set.from_class_to_set() == {'a', frozenset({'d', 'e', frozenset({'f',})})}
    assert res.my_set.from_class_to_set() == {frozenset({'c'})}


def test_another_operations():
    a = Constants()
    a.read_line('A = {a, b, {c}, {d, e, {f}}}')
    res1 = Constants()
    res1.read_line('A')

    b = Sets_and_operations()
    res = b.solution("{a, b, {c}, {d, f}} * ({a, b, {g}} + {{d, f}} / {a})")

    assert Another_operations.size(res1.my_set) == 4
    assert Another_operations.size(res) == 2

    assert Another_operations.psp(res1.my_set) == 6
    assert Another_operations.psp(res) == 3

    assert Another_operations.get_element(res1.my_set, 3).from_class_to_set() == {'d', 'e', frozenset({'f'})}
    assert Another_operations.get_element(res, 0).from_class_to_set() == {'b'}
