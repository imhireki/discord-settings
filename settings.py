from typing import Any
import json

from iter import iterator
from api.client import RequestClientV9


SettingIterator = iterator.ISettingIterator|iterator.IteratorManager


class DiscordSettings:
    _settings: dict = {}

    def __init__(self, request_client: RequestClientV9) -> None:
        self._request_client: RequestClientV9 = request_client

    def update(self, settings: dict) -> None:
        self._update_local()
        settings_before_update = {**self._settings}
        self._settings.update(settings)

        if settings_before_update == self._settings:
            return
        self._update_remote()

    def _update_remote(self) -> None:
        self._request_client.patch(self._settings)

    def _update_local(self) -> None:
        self._settings.update(
            json.loads(self._request_client.get().text))


class SettingsBuffer:
    def __init__(self, *iterators: SettingIterator) -> None:
        self._iterators: tuple[SettingIterator, ...] = iterators

    def _add_data_to_settings(self, settings: dict,
                              data: dict) -> dict:
        for key, value in data.items():
            if not key in settings:
                settings.update(data)
            else:
                settings[key].update(value)
        return settings

    def get_updated_buffer(self) -> dict:
        settings: dict = {}

        for iterator in self._iterators:
            self._add_data_to_settings(
                settings,
                iterator.iterable.get_request_data(next(iterator)))  # type: ignore
        return settings
