from collections.abc import Iterable
from abc import abstractmethod
from typing import Dict, List, Union

from iterators import iterator


class ISettingIterable(Iterable):
    """Interface to define a collection for the fields from the API."""

    def __init__(self, items: Union[List[str], str]):
        self._items = items

    def __iter__(self):
        """Default iterator. Never run out of items."""
        return iterator.Unlimited(self._items)

    @abstractmethod
    def name(self, value: str):
        """Set the dynamic 'name' for the requests."""
        pass


class EmojiName(ISettingIterable):
    """Emoji setting."""

    def name(self, value: str):
        return {'custom_status': {'emoji_name': f'{value}'}}


class Text(ISettingIterable):
    """Text setting."""

    def name(self, value: str):
        return {'custom_status': {'text': f'{value}'}}

    def multiple_before_index(self) -> iterator.MultipleBeforeIndex:
        """Custom iterator."""
        return iterator.MultipleBeforeIndex(self._items)

class Status(ISettingIterable):
    """Status setting."""

    def __init__(self):
        self._items = ['online', 'idle', 'dnd']

    def name(self, value: str):
        return {'status': f'{value}'}
