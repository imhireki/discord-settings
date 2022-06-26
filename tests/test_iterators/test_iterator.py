import pytest

from iterators import iterator
from typing import Union


@pytest.fixture
def iterable_items():
    return ["xyz", "abc"]

@pytest.fixture
def iterable_mock(mocker, iterable_items):
    def get_request_data(value):
        return {"test": value}
    return mocker.Mock(items=iterable_items, get_request_data=get_request_data)

@pytest.fixture
def request_data_value():
    return '123'

@pytest.fixture
def iterator_mock(iterable_mock):
    class Iterator:
        def __init__(self) -> None:
            self.iterable = iterable_mock
            self.collection: Union[str, tuple, list] = self.set_collection(self.iterable)
            self.max_collection_index: int = len(self.collection) - 1

        def set_collection(self, iterable) -> Union[str, tuple, list]:
            return iterable if isinstance(iterable, (list, tuple)) else iterable.items

        def get_request_data(self, value: str) -> dict[str, str]:
            return self.iterable.get_request_data(value)

        def indexes_in_collection_range(self, index: int, max_index: int) -> bool:
            return True if 0 <= index <= max_index else False

        def __next__(self) -> str:
            self.set_next_collection_index()

            if not self.indexes_in_collection_range(self.collection_index,
                                                    self.max_collection_index):
                self.reset_collection_index()

            return self.get_collection_item()

        def get_collection_item(self) -> str:
            return self.collection[self.collection_index]

        def set_next_collection_index(self) -> None:
            if not hasattr(self, 'collection_index'):
                return self.reset_collection_index()
            self.collection_index += 1

        def reset_collection_index(self) -> None:
            self.collection_index = 0

    return Iterator

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
