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

    def indexes_in_iterable_range(self, index, max_index):
        return True if 0 <= index <= max_index else False


class IUnlimitedItems(ISettingIterator):
    def __init__(self, iterable):
        self.iterable = iterable
        self.max_iterable_index = len(self.iterable) - 1

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


class Decrease(IUnlimitedItems):
    """[abc, xyz]  =  xyz -> abc"""

    def get_iterable_item(self):
        return self.iterable[self.iterable_index]

    def set_next_iterable_index(self):
        if not hasattr(self, 'iterable_index'):
            return self.reset_iterable_index()
        self.iterable_index -= 1

    def reset_iterable_index(self):
        self.iterable_index = self.max_iterable_index


class IUnlimitedItemsDecorator(ISettingIterator):
    def __init__(self, iterator):
        self.iterator = iterator

    def set_next_iterable(self):
        self.iterable = next(self.iterator)

    def is_first_loop(self):
        return True if not hasattr(self, 'iterable') else False

    def __next__(self):
        if self.is_first_loop():
            self.set_next_iterable()
            self.max_iterable_index = len(self.iterable) - 1

        self.set_next_iterable_index()

        if not self.indexes_in_iterable_range(self.iterable_index,
                                              self.max_iterable_index):
            self.set_next_iterable()
            self.max_iterable_index = len(self.iterable) - 1
            self.reset_iterable_index()

        return self.get_iterable_item()


class SingleItem(IUnlimitedItemsDecorator):
    """xyz          =  x -> y -> z"""

    def get_iterable_item(self):
        return self.iterable[self.iterable_index]

    def set_next_iterable_index(self):
        if not hasattr(self, 'iterable_index'):
            return self.reset_iterable_index()
        self.iterable_index += 1

    def reset_iterable_index(self):
        self.iterable_index = 0
