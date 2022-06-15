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

