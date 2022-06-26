from typing import Union

import pytest

from iterators import iterator


def test_increase(iterable_mock, iterable_items, request_data_value):
    increase_iterator = iterator.Increase(iterable_mock)
    request_data = increase_iterator.get_request_data(request_data_value)

    assert request_data == iterable_mock.get_request_data(request_data_value)

    assert next(increase_iterator) == iterable_items[0]
    assert next(increase_iterator) == iterable_items[1]
    assert next(increase_iterator) == iterable_items[0]

def test_decrease(iterable_mock, iterable_items, request_data_value):
    decrease_iterator = iterator.Decrease(iterable_mock)
    request_data = decrease_iterator.get_request_data(request_data_value)

    assert request_data == iterable_mock.get_request_data(request_data_value)

    assert next(decrease_iterator) == iterable_items[1]
    assert next(decrease_iterator) == iterable_items[0]
    assert next(decrease_iterator) == iterable_items[1]

def test_single_item(iterable_items, iterator_mock):
    _iterator = iterator_mock()
    single_item_iterator = iterator.SingleItem(_iterator)

    assert next(single_item_iterator) == iterable_items[0][0]
    assert next(single_item_iterator) == iterable_items[0][1]
    assert next(single_item_iterator) == iterable_items[0][2]
    assert next(single_item_iterator) == iterable_items[1][0]

def test_items_before_next_index(iterable_items, iterator_mock):
    _iterator = iterator_mock()
    items_before_next_index_iterator = iterator.ItemsBeforeNextIndex(_iterator)

    assert next(items_before_next_index_iterator) == iterable_items[0][:1]
    assert next(items_before_next_index_iterator) == iterable_items[0][:2]
    assert next(items_before_next_index_iterator) == iterable_items[0][:3]
    assert next(items_before_next_index_iterator) == iterable_items[1][:1]

def test_items_after_index(iterable_items, iterator_mock):
    _iterator = iterator_mock()
    items_after_index_iterator = iterator.ItemsAfterIndex(_iterator)

    assert next(items_after_index_iterator) == iterable_items[0][-1:]
    assert next(items_after_index_iterator) == iterable_items[0][-2:]
    assert next(items_after_index_iterator) == iterable_items[0][-3:]
    assert next(items_after_index_iterator) == iterable_items[1][-1:]

def test_iterator_manager(iterable_items, iterator_mock):
    prefix_iterator = iter(iterable_items[1])
    _iterator = iterator_mock()
    suffix_iterator = iter(iterable_items[1])

    iterator_manager = iterator.IteratorManager(_iterator, prefix_iterator, suffix_iterator)

    assert next(iterator_manager) == iterable_items[1][0] + iterable_items[0] + iterable_items[1][0]
    assert next(iterator_manager) == iterable_items[1][1] + iterable_items[1] + iterable_items[1][1]
    assert next(iterator_manager) == iterable_items[1][2] + iterable_items[0] + iterable_items[1][2]
