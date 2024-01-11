import json

import settings


def test_discord_settings(mocker):
    remote_settings = '{"status": "dnd", "custom_status": {"text": "xD"}}'
    new_settings = {"status": "online", "a": "1"}
    remote_settings_updated = {**json.loads(remote_settings), **new_settings}
    request_client_mock = mocker.Mock(get=mocker.Mock(
        return_value=mocker.Mock(text=remote_settings)))

    local_settings = settings.DiscordSettings(request_client_mock)
    local_settings.update(new_settings)

    assert local_settings._settings == remote_settings_updated

def test_settings_buffer(mocker, make_setting_iterable):
    setting_a = make_setting_iterable(id='a', items=['1', '2'])
    setting_b = make_setting_iterable(id='b', items=['x', 'y'])
    expected_buffer_1 = {"setting": {"a": "1", "b": "x"}}
    expected_buffer_2 = {"setting": {"a": "2", "b": "y"}}

    settings_buffer = settings.SettingsBuffer(iter(setting_a), iter(setting_b))
    buffer_1 = settings_buffer.get_updated_buffer()
    buffer_2 = settings_buffer.get_updated_buffer()

    assert buffer_1 == expected_buffer_1
    assert buffer_2 == expected_buffer_2
