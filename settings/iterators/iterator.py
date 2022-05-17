from collections.abc import Iterator
from typing import Union


class ISettingIterator(Iterator):
    """Interface to define iterators for the settings (iterable)."""

    def __init__(self, collection: Union[list, str]):
        self._collection = collection


class Unlimited(ISettingIterator):
    """Default iterator, never run out of items."""
    _index = 0

    def _get_next_item(self):
        item = self._collection[self._index]
        self._index += 1
        return item

    def __next__(self):
        if self._index > (len(self._collection) - 1):
            self._index = 0
        return self._get_next_item()


class BeforeIndex(ISettingIterator):
    """Get all the items before the index."""
    _index = 0

    def _get_next_item(self):
        item = self._collection[:(self._index) + 1]
        self._index += 1
        return item

    def __next__(self):
        if self._index > (len(self._collection) - 1):
            self._index = 0
        return self._get_next_item()


class MultipleBeforeIndex(ISettingIterator):
    """A BeforeIndex, support to multiple collections."""
    _index = 0
    _collection_index = 0

    def get_next_item(self):
        item = self._collection[self._collection_index][:(self._index) + 1]
        self._index += 1
        return item

    def get_collection_index(self):
        """Get the actual collection (index)"""
        return len(self._collection) - 1

    def get_collection_item_index(self):
        """Get the actual item from a collection (index)"""
        return len(self._collection[self._collection_index]) - 1

    def __next__(self):
        if self._index > self.get_collection_item_index():
            # Change Indexes
            self._index = 0  # Reset
            self._collection_index += 1  # Move to the next collection

            # Reset the collection index if out of range.
            if self._collection_index > self.get_collection_index():
                self._collection_index = 0

        return self.get_next_item()


class Prefix(Iterator):
    """Decorator. Add to a Iterator a prefix."""

    _index = 0

    def __init__(self, iterator, collection):
        self._iterator = iterator
        self._collection = collection

    def get_next_item(self):
        item = self._collection[self._index]
        self._index += 1
        return item

    def __next__(self):
        iterator_result = self._iterator.__next__()

        if self._index > (len(self._collection) - 1):
            self._index = 0
        return f'{self.get_next_item()}{iterator_result}'


class Suffix(Iterator):
    """Decorator. Add to a Iterator a suffix"""
    _index = 0

    def __init__(self, iterator, collection):
        self._iterator = iterator
        self._collection = collection

    def get_next_item(self):
        item = self._collection[self._index]
        self._index += 1
        return item

    def __next__(self):
        iterator_result = self._iterator.__next__()

        if self._index > (len(self._collection) - 1):
            self._index = 0
        return f'{iterator_result}{self.get_next_item()}'
