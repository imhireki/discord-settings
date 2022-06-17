import pytest

from iterators import iterator


def test_increase():
    iterable = ["abc", "xyz"]
    increase_iterator = iterator.Increase(iterable)

    assert next(increase_iterator) == iterable[0]
    assert next(increase_iterator) == iterable[1]

    assert next(increase_iterator) == iterable[0]
    # StopIteration not raised !
