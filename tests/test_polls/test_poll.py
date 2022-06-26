from polls import poll
import pytest


@pytest.mark.parametrize('updated_buffer', [{"x": "a"}, {"y": "b"}])
def test_poll(mocker, updated_buffer):

    def get_updated_buffer():
        return updated_buffer

    buffer = mocker.Mock(get_updated_buffer=get_updated_buffer)

    class LocalSettings:
        _settings = {}

        def update(self, settings):
            self._settings.update(settings)

    def polling():
        settings.update(buffer.get_updated_buffer())

    settings = LocalSettings()

    _poll = poll.Poll(settings, buffer)
    mocker.patch.object(_poll, 'polling', return_value=polling())

    _poll.polling()

    assert settings._settings == updated_buffer
