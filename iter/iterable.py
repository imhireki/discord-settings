from collections.abc import Iterable
from abc import abstractmethod

from iter import iterator


class ISettingIterable(Iterable):
    def __init__(self, items: tuple | list) -> None:
        self.items: tuple | list = items

    @abstractmethod
    def get_request_data(self, value: str) -> dict: pass

    def __iter__(self) -> iterator.Increase:
        return self.increase()

    def increase(self) -> iterator.Increase:
        return iterator.Increase(self)

    def decrease(self) -> iterator.Decrease:
        return iterator.Decrease(self)


class EmojiName(ISettingIterable):
    def get_request_data(self, value: str) -> dict:
        return {'custom_status': {'emoji_name': value}}


class Text(ISettingIterable):
    def get_request_data(self, value: str) -> dict:
        return {'custom_status': {'text': value}}


class Status(ISettingIterable):
    def __init__(self, items: tuple | list = []) -> None:
        super().__init__(items or ['online', 'idle', 'dnd'])

    def get_request_data(self, value: str) -> dict:
        return {'status': value}
