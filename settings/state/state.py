from discord.api import DiscordSettingsAPI
from iterators.iterator import ISettingIterator
from iterables.iterable import ISettingIterable
from typing import Dict, List

from copy import deepcopy


class Settings:
    """Keep the state of the local settings.

    TODO: Update the local state from remote.
    """

    _state: Dict[str, str] = {}

    def __init__(self, settings_api: DiscordSettingsAPI):
        self.settings_api = settings_api

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, settings: Dict[str, str]):
        """Update the remote settings if necessary."""

        actual_state = deepcopy(self._state)
        self._state.update(settings)

        if actual_state == self._state:
            return

        self.update_remote()

    def update_remote(self):
        """Patch the remote settings."""
        self.settings_api.patch(self._state)

    def update_local(self): pass


class Buffer:
    """Handle the data from multiple sources."""

    def __init__(self, iterables: List[ISettingIterable],
                 iterators: List[ISettingIterator]):

        self._iterables = iterables
        self._iterators = iterators

    def update_or_create_key(self, settings: Dict[str, str],
                             name: Dict[str, str]):
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

        settings: Dict[str, str] = {}

        for iterator, iterable in zip(self._iterators, self._iterables):
            name = iterable.name(next(iterator))
            settings = self.update_or_create_key(settings, name)

        return settings

