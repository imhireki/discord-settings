from typing import Any
import json

from iter.iterator import ISettingIterator
from api.client import IRequestClient


DiscordSettings = dict[str, Any]


class LocalSettings:
    _settings: DiscordSettings = {}

    def __init__(self, request_client: IRequestClient) -> None:
        self._request_client: IRequestClient = request_client

    def update(self, settings: DiscordSettings) -> None:
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
    def __init__(self, *iterators: ISettingIterator) -> None:
        self._iterators: list[ISettingIterator] = iterators

    def _add_data_to_settings(self, settings: DiscordSettings,
                              data: DiscordSettings) -> DiscordSettings:
        for key, value in data.items():
            if not key in settings:
                settings.update(data)
            else:
                settings[key].update(value)
        return settings

    def get_updated_buffer(self) -> DiscordSettings:
        settings: DiscordSettings = {}

        for iterator in self._iterators:
            self._add_data_to_settings(
                settings, iterator.iterable.get_request_data(next(iterator)))
        return settings
