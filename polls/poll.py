from state.state import Settings, Buffer
from time import sleep


class Poll:
    """Loop management."""

    def __init__(self, settings: Settings, buffer: Buffer):
        self._settings = settings
        self._buffer = buffer

    def polling(self, timeout=3):
        """Update the settings' state."""

        while True:
            self._settings.state = self._buffer.get_updated_buffer()
            sleep(timeout)
