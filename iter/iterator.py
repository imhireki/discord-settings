from typing import Iterable, Iterator
from abc import ABC, abstractmethod
from typing import Optional


class ISettingIterator(ABC):
    _max_collection_index: int
    _collection_index: int
    iterable: Iterable

    def __iter__(self): return self

    @abstractmethod
    def __next__(self) -> str: pass

    @abstractmethod
    def _get_collection_item(self) -> str: pass

    @abstractmethod
    def _set_next_collection_index(self) -> None: pass

    @abstractmethod
    def _reset_collection_index(self) -> None: pass

    def _indexes_in_collection_range(self, index: int, max_index: int) -> bool:
        return True if 0 <= index <= max_index else False


class IUnlimitedItems(ISettingIterator):
    def __init__(self, iterable: Iterable) -> None:
        self.iterable: Iterable = iterable
        self._collection: tuple | list = self._set_collection(self.iterable)
        self._max_collection_index = len(self._collection) - 1

    def _set_collection(self, iterable: Iterable) -> tuple | list:
        is_setting_iterable = not isinstance(iterable, (list, tuple))
        return iterable.items if is_setting_iterable else iterable  # type: ignore

    def get_request_data(self, value: str) -> dict[str, str]:
       return self.iterable.get_request_data(value)  # type: ignore

    def __next__(self) -> str:
        self._set_next_collection_index()
        if not self._indexes_in_collection_range(self._collection_index,
                                                 self._max_collection_index):
            self._reset_collection_index()
        return self._get_collection_item()


class Increase(IUnlimitedItems):
    """[abc, xyz]  =  abc -> xyz"""

    def _get_collection_item(self) -> str:
        return self._collection[self._collection_index]

    def _set_next_collection_index(self) -> None:
        if not hasattr(self, '_collection_index'):
            return self._reset_collection_index()
        self._collection_index += 1

    def _reset_collection_index(self) -> None:
        self._collection_index = 0


class Decrease(IUnlimitedItems):
    """[abc, xyz]  =  xyz -> abc"""

    def _get_collection_item(self) -> str:
        return self._collection[self._collection_index]

    def _set_next_collection_index(self) -> None:
        if not hasattr(self, '_collection_index'):
            return self._reset_collection_index()
        self._collection_index -= 1

    def _reset_collection_index(self) -> None:
        self._collection_index = self._max_collection_index


class IUnlimitedItemsDecorator(ISettingIterator):
    _collection: str

    def __init__(self, iterator: IUnlimitedItems) -> None:
        self.iterator: IUnlimitedItems = iterator
        self.iterable: Iterable = iterator.iterable

    def _is_first_loop(self) -> bool:
        return True if not hasattr(self, '_collection') else False

    def __next__(self) -> str:
        if self._is_first_loop():
            self._collection = next(self.iterator)
            self._max_collection_index = len(self._collection) - 1

        self._set_next_collection_index()

        if not self._indexes_in_collection_range(self._collection_index,
                                                 self._max_collection_index):
            self._collection = next(self.iterator)
            self._max_collection_index = len(self._collection) - 1
            self._reset_collection_index()

        return self._get_collection_item()


class SingleItem(IUnlimitedItemsDecorator):
    """xyz  =  x -> y -> z"""

    def _get_collection_item(self) -> str:
        return self._collection[self._collection_index]

    def _set_next_collection_index(self) -> None:
        if not hasattr(self, '_collection_index'):
            return self._reset_collection_index()
        self._collection_index += 1

    def _reset_collection_index(self) -> None:
        self._collection_index = 0


class ItemsBeforeNextIndex(IUnlimitedItemsDecorator):
    """xyz  =  x -> xy -> xyz"""

    def _get_collection_item(self) -> str:
        return self._collection[:self._collection_index + 1]

    def _set_next_collection_index(self) -> None:
        if not hasattr(self, '_collection_index'):
            return self._reset_collection_index()
        self._collection_index += 1

    def _reset_collection_index(self) -> None:
        self._collection_index = 0


class ItemsAfterIndex(IUnlimitedItemsDecorator):
    """xyz  =  z -> yz -> xyz"""

    def _get_collection_item(self) -> str:
        return self._collection[
            self._collection_index : self._max_collection_index + 1
            ]

    def _set_next_collection_index(self) -> None:
        if not hasattr(self, '_collection_index'):
            return self._reset_collection_index()
        self._collection_index -= 1

    def _reset_collection_index(self) -> None:
        self._collection_index = self._max_collection_index


class UpperIndexItem(IUnlimitedItemsDecorator):
    """xyz  =  Xyz -> xYz -> xyZ"""

    def _get_collection_item(self) -> str:
        return ''.join([
            item.upper() if index == self._collection_index else item
            for index, item in enumerate(self._collection)
        ])

    def _set_next_collection_index(self) -> None:
        if not hasattr(self, '_collection_index'):
            return self._reset_collection_index()
        self._collection_index += 1

    def _reset_collection_index(self) -> None:
        self._collection_index = 0


class IteratorManager:
    def __init__(self, iterator: ISettingIterator,
                 prefix_iterator: Optional[Iterator] = None,
                 suffix_iterator: Optional[Iterator] = None) -> None:

        self.iterator: ISettingIterator = iterator
        self.iterable: Iterable = iterator.iterable
        self._prefix_iterator: Iterator|None = prefix_iterator
        self._suffix_iterator: Iterator|None = suffix_iterator

    def _get_iterators_result(self) -> list | tuple:
        return [
            item for item in [
                next(self._prefix_iterator) if self._prefix_iterator else None,
                next(self.iterator),
                next(self._suffix_iterator) if self._suffix_iterator else None
            ]
            if item
        ]

    def __next__(self) -> str:
        iterators_result = self._get_iterators_result()
        iterators_result_string = ''.join(iterators_result)
        return iterators_result_string
