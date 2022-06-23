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

def test_decrease():
    iterable = ["abc", "xyz"]
    decrease_iterator = iterator.Decrease(iterable)

    assert next(decrease_iterator) == iterable[1]
    assert next(decrease_iterator) == iterable[0]
    assert next(decrease_iterator) == iterable[1]

def test_single_item():
    iterable = ["abc"]
    abc_iterator = iter(iterable)

    single_item_iterator = iterator.SingleItem(abc_iterator)

    assert next(single_item_iterator) == iterable[0][0]
    assert next(single_item_iterator) == iterable[0][1]
    assert next(single_item_iterator) == iterable[0][2]

def test_items_before_next_index():
    iterable = ["xyz"]
    xyz_iterator = iter(iterable)

    items_before_next_index_iterator = iterator.ItemsBeforeNextIndex(xyz_iterator)

    assert next(items_before_next_index_iterator) == iterable[0][:1]
    assert next(items_before_next_index_iterator) == iterable[0][:2]
    assert next(items_before_next_index_iterator) == iterable[0][:3]
