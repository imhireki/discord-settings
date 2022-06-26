from copy import deepcopy
import json

import pytest

from settings import settings
from iterables import iterable


def test_local_settings(mocker):
    remote_settings = '{"status": "dnd", "custom_status": {"text": "xD"}}'
    new_settings = {"status": "online", "a": "1"}

    remote_settings_updated = deepcopy(json.loads(remote_settings))
    remote_settings_updated.update(new_settings)

    response_mock = mocker.Mock(text=remote_settings)
    request_client_mock = mocker.Mock(get=mocker.Mock(return_value=response_mock))

    local_settings = settings.LocalSettings(request_client_mock)
    local_settings.update(new_settings)

    assert local_settings._settings == remote_settings_updated

def test_settings_buffer(mocker):
    class SettingA(iterable.ISettingIterable):
        def __init__(self) -> None:
            super().__init__(["1", "2", "3"])

        def get_request_data(self, value: str) -> dict[str, str]:
            return {"setting": {"a": value}}


    class SettingB(iterable.ISettingIterable):
        def __init__(self) -> None:
            super().__init__(["x", "y", "z"])

        def get_request_data(self, value: str) -> dict[str, str]:
            return {"setting": {"b": value}}

    setting_a = SettingA()
    setting_a_iter = iter(setting_a)

    setting_b = SettingB()
    setting_b_iter = iter(setting_b)

    settings_buffer = settings.SettingsBuffer(setting_a_iter, setting_b_iter)

    for item_a, item_b in zip(setting_a.items, setting_b.items):
        assert settings_buffer.get_updated_buffer() == {
            "setting": {"a": item_a, "b": item_b}
        }
