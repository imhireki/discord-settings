from settings import settings
from time import sleep


class Poll:
    def __init__(self, settings: settings.LocalSettings, buffer: settings.SettingsBuffer) -> None:
        self._settings: settings.LocalSettings = settings
        self._buffer: settings.SettingsBuffer = buffer

    def polling(self, timeout: int = 3) -> None:
        while True:
            updated_buffer = self._buffer.get_updated_buffer()
            self._settings.update(updated_buffer)
            sleep(timeout)
