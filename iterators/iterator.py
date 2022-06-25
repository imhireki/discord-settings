from abc import ABC, abstractmethod


class ISettingIterator(ABC):
    def __init__(self):
        collection: object
        max_collection_index: int
        collection_index: int

    @abstractmethod
    def __next__(self): pass

    @abstractmethod
    def get_collection_item(self): pass

    @abstractmethod
    def set_next_collection_index(self): pass

    @abstractmethod
    def reset_collection_index(self): pass

    def indexes_in_collection_range(self, index, max_index):
        return True if 0 <= index <= max_index else False


class IUnlimitedItems(ISettingIterator):
    def __init__(self, iterable):
        self.iterable = iterable
        self.collection = self.iterable._items
        self.max_collection_index = len(self.collection) - 1

    def get_request_data(self, value):
       return self.iterable.get_request_data(value)

    def __next__(self):
        self.set_next_collection_index()

        if not self.indexes_in_collection_range(self.collection_index,
                                                self.max_collection_index):
            self.reset_collection_index()

        return self.get_collection_item()


class Increase(IUnlimitedItems):
    """[abc, xyz]  =  abc -> xyz"""

    def get_collection_item(self):
        return self.collection[self.collection_index]

    def set_next_collection_index(self):
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index += 1

    def reset_collection_index(self):
        self.collection_index = 0


class Decrease(IUnlimitedItems):
    """[abc, xyz]  =  xyz -> abc"""

    def get_collection_item(self):
        return self.collection[self.collection_index]

    def set_next_collection_index(self):
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index -= 1

    def reset_collection_index(self):
        self.collection_index = self.max_collection_index


class IUnlimitedItemsDecorator(ISettingIterator):
    def __init__(self, iterator):
        self.iterator = iterator

    def set_next_collection(self):
        self.collection = next(self.iterator)

    def is_first_loop(self):
        return True if not hasattr(self, 'collection') else False

    def __next__(self):
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

    def get_collection_item(self):
        return self.collection[self.collection_index]

    def set_next_collection_index(self):
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index += 1

    def reset_collection_index(self):
        self.collection_index = 0


class ItemsBeforeNextIndex(IUnlimitedItemsDecorator):
    """xyz  =  x -> xy -> xyz"""

    def get_collection_item(self):
        return self.collection[:self.collection_index + 1]

    def set_next_collection_index(self):
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index += 1

    def reset_collection_index(self):
        self.collection_index = 0


class ItemsAfterIndex(IUnlimitedItemsDecorator):
    """xyz  =  z -> yz -> xyz"""

    def get_collection_item(self):
        return self.collection[self.collection_index:self.max_collection_index + 1]

    def set_next_collection_index(self):
        if not hasattr(self, 'collection_index'):
            return self.reset_collection_index()
        self.collection_index -= 1

    def reset_collection_index(self):
        self.collection_index = self.max_collection_index


class IteratorManager:
    def __init__(self, iterator, prefix_iterator=None, suffix_iterator=None):
        self.iterator = iterator
        self.prefix_iterator = prefix_iterator
        self.suffix_iterator = suffix_iterator

    def get_iterators_result(self):
        return [
            item for item in [
                next(self.prefix_iterator) if self.prefix_iterator else None,
                next(self.iterator),
                next(self.suffix_iterator) if self.suffix_iterator else None]
            if item
        ]

    def __next__(self):
        iterators_result = self.get_iterators_result()
        iterators_result_string = ''.join(iterators_result)
        return iterators_result_string
