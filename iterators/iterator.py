from abc import ABC, abstractmethod


class ISettingIterator(ABC):
    def __init__(self):
        iterable: object
        max_iterable_index: int
        iterable_index: int

    @abstractmethod
    def __next__(self): pass

    @abstractmethod
    def get_iterable_item(self): pass

    @abstractmethod
    def set_next_iterable_index(self): pass

    @abstractmethod
    def reset_iterable_index(self): pass


class IUnlimitedItems(ISettingIterator):
    def __init__(self, iterable):
        self.iterable = iterable
        self.max_iterable_index = len(self.iterable) - 1

    def indexes_in_iterable_range(self, index, max_index):
        return True if 0 <= index <= max_index else False

    def __next__(self):
        self.set_next_iterable_index()

        if not self.indexes_in_iterable_range(self.iterable_index,
                                              self.max_iterable_index):
            self.reset_iterable_index()

        return self.get_iterable_item()


class Increase(IUnlimitedItems):
    """[abc, xyz]  =  abc -> xyz"""

    def get_iterable_item(self):
        return self.iterable[self.iterable_index]

    def set_next_iterable_index(self):
        if not hasattr(self, 'iterable_index'):
            return self.reset_iterable_index()
        self.iterable_index += 1

    def reset_iterable_index(self):
        self.iterable_index = 0
