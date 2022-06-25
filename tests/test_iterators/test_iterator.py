import pytest

from iterators import iterator


@pytest.fixture
def iterable_items():
    return ["xyz", "abc"]

@pytest.fixture
def iterable(mocker, iterable_items):
    def get_request_data(value):
        return {"test": value}
    return mocker.Mock(_items=iterable_items, get_request_data=get_request_data)

@pytest.fixture
def request_data_value():
    return '123'

def test_increase(iterable, iterable_items, request_data_value):
    increase_iterator = iterator.Increase(iterable)
    request_data = increase_iterator.get_request_data(request_data_value)

    assert request_data == iterable.get_request_data(request_data_value)

    assert next(increase_iterator) == iterable_items[0]
    assert next(increase_iterator) == iterable_items[1]
    assert next(increase_iterator) == iterable_items[0]

def test_decrease(iterable, iterable_items, request_data_value):
    decrease_iterator = iterator.Decrease(iterable)
    request_data = decrease_iterator.get_request_data(request_data_value)

    assert request_data == iterable.get_request_data(request_data_value)

    assert next(decrease_iterator) == iterable_items[1]
    assert next(decrease_iterator) == iterable_items[0]
    assert next(decrease_iterator) == iterable_items[1]

def test_single_item(iterable_items):
    _iterator = iter(iterable_items)
    single_item_iterator = iterator.SingleItem(_iterator)

    assert next(single_item_iterator) == iterable_items[0][0]
    assert next(single_item_iterator) == iterable_items[0][1]
    assert next(single_item_iterator) == iterable_items[0][2]
    assert next(single_item_iterator) == iterable_items[1][0]

def test_items_before_next_index(iterable_items):
    _iterator = iter(iterable_items)
    items_before_next_index_iterator = iterator.ItemsBeforeNextIndex(_iterator)

    assert next(items_before_next_index_iterator) == iterable_items[0][:1]
    assert next(items_before_next_index_iterator) == iterable_items[0][:2]
    assert next(items_before_next_index_iterator) == iterable_items[0][:3]
    assert next(items_before_next_index_iterator) == iterable_items[1][:1]

def test_items_after_index(iterable_items):
    _iterator = iter(iterable_items)
    items_after_index_iterator = iterator.ItemsAfterIndex(_iterator)

    assert next(items_after_index_iterator) == iterable_items[0][-1:]
    assert next(items_after_index_iterator) == iterable_items[0][-2:]
    assert next(items_after_index_iterator) == iterable_items[0][-3:]
    assert next(items_after_index_iterator) == iterable_items[1][-1:]

def test_iterator_manager(iterable_items):
    prefix_iterator = iter(iterable_items[1])
    _iterator = iter(iterable_items[0])
    suffix_iterator = iter(iterable_items[1])

    iterator_manager = iterator.IteratorManager(_iterator, prefix_iterator, suffix_iterator)

    assert next(iterator_manager) == iterable_items[1][0] + iterable_items[0][0] + iterable_items[1][0]
    assert next(iterator_manager) == iterable_items[1][1] + iterable_items[0][1] + iterable_items[1][1]
    assert next(iterator_manager) == iterable_items[1][2] + iterable_items[0][2] + iterable_items[1][2]
