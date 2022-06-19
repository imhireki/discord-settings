import pytest

from iterators import iterator


def test_increase():
    iterable = ["abc", "xyz"]
    increase_iterator = iterator.Increase(iterable)

    assert next(increase_iterator) == iterable[0]
    assert next(increase_iterator) == iterable[1]
    assert next(increase_iterator) == iterable[0]


def test_decrease():
    iterable = ["abc", "xyz"]
    decrease_iterator = iterator.Decrease(iterable)

    assert next(decrease_iterator) == iterable[1]
    assert next(decrease_iterator) == iterable[0]
    assert next(decrease_iterator) == iterable[1]
