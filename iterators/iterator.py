from abc import ABC, abstractmethod
from typing import Union, Iterable, Iterator


class ISettingIterator(ABC):
    def __init__(self) -> None:
        collection: Union[list, tuple]
        max_collection_index: int
        collection_index: int

    @abstractmethod
    def __next__(self) -> str: pass

    @abstractmethod
    def get_collection_item(self) -> str: pass

    @abstractmethod
    def set_next_collection_index(self) -> None: pass

    @abstractmethod
    def reset_collection_index(self) -> None: pass

    def indexes_in_collection_range(self, index: int, max_index: int) -> bool:
        return True if 0 <= index <= max_index else False


class IUnlimitedItems(ISettingIterator):
    def __init__(self, iterable: Iterable) -> None:
        self.iterable: Iterable = iterable
        self.collection: Union[str, tuple, list] = self.set_collection(self.iterable)
        self.max_collection_index: int = len(self.collection) - 1

    def set_collection(self, iterable: Iterable) -> Union[str, tuple, list]:
        return iterable if isinstance(iterable, (list, tuple)) else iterable.items

    def get_request_data(self, value: str) -> dict[str, str]:
       return self.iterable.get_request_data(value)

    def __next__(self) -> str:
        self.set_next_collection_index()

        if not self.indexes_in_collection_range(self.collection_index,
                                                self.max_collection_index):
            self.reset_collection_index()

        return self.get_collection_item()


class Increase(IUnlimitedItems):
    """[abc, xyz]  =  abc -> xyz"""

    def get_collection_item(self) -> str:
        return self.collection[self.collection_index]

    def set_next_collection_index(self) -> None:
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index += 1

    def reset_collection_index(self) -> None:
        self.collection_index = 0


class Decrease(IUnlimitedItems):
    """[abc, xyz]  =  xyz -> abc"""

    def get_collection_item(self) -> str:
        return self.collection[self.collection_index]

    def set_next_collection_index(self) -> None:
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index -= 1

    def reset_collection_index(self) -> None:
        self.collection_index = self.max_collection_index


class IUnlimitedItemsDecorator(ISettingIterator):
    def __init__(self, iterator: IUnlimitedItems):
        self.iterator: IUnlimitedItems = iterator

    def set_next_collection(self) -> None:
        self.collection: str = next(self.iterator)

    def is_first_loop(self) -> bool:
        return True if not hasattr(self, 'collection') else False

    def __next__(self) -> str:
        if self.is_first_loop():
            self.set_next_collection()
            self.max_collection_index = len(self.collection) - 1

        self.set_next_collection_index()

        if not self.indexes_in_collection_range(self.collection_index,
                                                self.max_collection_index):
            self.set_next_collection()
            self.max_collection_index = len(self.collection) - 1
            self.reset_collection_index()

        return self.get_collection_item()


class SingleItem(IUnlimitedItemsDecorator):
    """xyz  =  x -> y -> z"""

    def get_collection_item(self) -> str:
        return self.collection[self.collection_index]

    def set_next_collection_index(self) -> None:
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index += 1

    def reset_collection_index(self) -> None:
        self.collection_index = 0


class ItemsBeforeNextIndex(IUnlimitedItemsDecorator):
    """xyz  =  x -> xy -> xyz"""

    def get_collection_item(self) -> str:
        return self.collection[:self.collection_index + 1]

    def set_next_collection_index(self) -> None:
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index += 1

    def reset_collection_index(self) -> None:
        self.collection_index = 0


class ItemsAfterIndex(IUnlimitedItemsDecorator):
    """xyz  =  z -> yz -> xyz"""

    def get_collection_item(self) -> str:
        return self.collection[self.collection_index:self.max_collection_index + 1]

    def set_next_collection_index(self) -> None:
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index -= 1

    def reset_collection_index(self) -> None:
        self.collection_index = self.max_collection_index


class IteratorManager:
    def __init__(self, iterator: Iterator, prefix_iterator: Iterator = None,
                 suffix_iterator: Iterator = None) -> None:
        self.iterator: Iterator = iterator
        self.prefix_iterator: Iterator = prefix_iterator
        self.suffix_iterator: Iterator = suffix_iterator

    def get_iterators_result(self) -> Union[list, tuple]:
        return [
            item for item in [
                next(self.prefix_iterator) if self.prefix_iterator else None,
                next(self.iterator),
                next(self.suffix_iterator) if self.suffix_iterator else None]
            if item
        ]

    def __next__(self) -> str:
        iterators_result = self.get_iterators_result()
        iterators_result_string = ''.join(iterators_result)
        return iterators_result_string
