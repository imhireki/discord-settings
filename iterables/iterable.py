from collections.abc import Iterable
from iterators import iterator
from abc import abstractmethod
from typing import Union


class ISettingIterable(Iterable):
    def __init__(self, items: Union[list[str], str]) -> None:
        self._items: Union[list[str], str] = items

    @abstractmethod
    def get_request_data(value: str) -> dict[str, str]: pass

    def __iter__(self) -> iterator.Unlimited:
        return iterator.Unlimited(self._items)


class EmojiName(ISettingIterable):
    def get_request_data(self, value: str) -> dict[str, str]:
        return {'custom_status': {'emoji_name': value}}


class Text(ISettingIterable):
    def get_request_data(self, value: str) -> dict[str, str]:
        return {'custom_status': {'text': value}}

    def iter_data_before_index(self) -> iterator.MultipleBeforeIndex:
        return iterator.MultipleBeforeIndex(self._items)


class Status(ISettingIterable):
    def __init__(self) -> None:
        super().__init__(['online', 'idle', 'dnd'])

    def get_request_data(self, value: str):
        return {'status': value}
