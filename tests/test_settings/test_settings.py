from settings import settings
from copy import deepcopy
import json


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
