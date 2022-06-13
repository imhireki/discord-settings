from api.client import IRequestClient

from iterators.iterator import ISettingIterator
from iterables.iterable import ISettingIterable

from copy import deepcopy


class LocalSettings:
    _settings: dict[str, str] = {}

    def __init__(self, request_client: IRequestClient) -> None:
        self.request_client: IRequestClient = request_client

    def update(self, settings: dict[str, str]) -> None:

        self.update_local()
        settings_before_update = deepcopy(self._settings)

        self._settings.update(settings)

        if settings_before_update == self._settings:
            return

        self.update_remote()

    def update_remote(self) -> None:
        self.request_client.patch(self._settings)

    def update_local(self) -> None:
        response = self.request_client.get()
        self._settings.update(eval(response.text))


class Buffer:
    """Handle the data from multiple sources."""

    def __init__(self, iterables: list[ISettingIterable],
                 iterators: list[ISettingIterator]) -> None:
        self._iterables = iterables
        self._iterators = iterators

    def update_or_create_key(self, settings: dict[str, str], name: dict[str, str]):
        """Set the name in the settings."""

        for key, value in name.items():
            # Update the settings
            if not key in settings:
                settings.update(name)
            # Update the key
            else:
                settings[key].update(value)
        return settings

    def get_updated_buffer(self):
        """Return a buffer with the data ready to make a request."""

        settings: dict[str, str] = {}

        for iterator, iterable in zip(self._iterators, self._iterables):
            name = iterable.name(next(iterator))
            settings = self.update_or_create_key(settings, name)

        return settings

