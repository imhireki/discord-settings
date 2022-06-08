import pytest

from discord.api import *


@pytest.fixture
def endpoint():
    return 'http://test.test/'


class TestGet:
    def test_perform_get_request(self, requests_mock, auth_token, endpoint):
        headers = {'Authorization': auth_token}
        request_method = Get(endpoint, headers)

        text_data = '{"test": 123}'
        requests_mock.get(endpoint, text=text_data)

        response = request_method.perform_get_request()

        assert request_method.headers == headers
        assert response.status_code == 200
        assert response.url == endpoint
        assert response.text == text_data


class TestPatch:
    def test_perform_patch_request(self, requests_mock, auth_token, endpoint):
        headers = {
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        }
        request_method = Patch(endpoint, headers)
        requests_mock.patch(endpoint)

        response = request_method.perform_patch_request(data={'status': 'dnd'})

        assert request_method.headers == headers
        assert response.status_code == 200
        assert response.url == endpoint


class TestPatchRequest:
    def test_perform_request(self, mocker):
        perform_patch_request_mock = mocker.Mock()
        patch_request_method_mock = mocker.Mock(
            perform_patch_request=perform_patch_request_mock
        )

        patch_request = PatchRequest(patch_request_method_mock)

        patch_request.perform_request()

        assert perform_patch_request_mock.called


class TestGetRequest:
    def test_perform_request(self, mocker):
        perform_get_request_mock = mocker.Mock()
        get_request_method_mock = mocker.Mock(
            perform_get_request=perform_get_request_mock
        )

        get_request = GetRequest(get_request_method_mock)

        get_request.perform_request()

        assert perform_get_request_mock.called


class TestDiscordSettingsRequestClient:
    def test_set_request(self, mocker):
        settings_client = DiscordSettingsRequestClient()

        get_request_mock = mocker.Mock()
        patch_request_mock = mocker.Mock()

        settings_client.set_request('GET', get_request_mock)
        settings_client.set_request('PATCH', patch_request_mock)

        assert len(settings_client._requests) == 2
        assert settings_client._requests['GET'] == get_request_mock
        assert settings_client._requests['PATCH'] == patch_request_mock

    def test_perform_request(self, mocker):
        settings_client = DiscordSettingsRequestClient()

        get_perform_request_mock = mocker.Mock()
        get_request_mock = mocker.Mock(perform_request=get_perform_request_mock)

        patch_perform_request_mock = mocker.Mock()
        patch_request_mock = mocker.Mock(
            perform_request=patch_perform_request_mock
        )
        patch_data = {'data': 123}

        settings_client.set_request('GET', get_request_mock)
        settings_client.set_request('PATCH', patch_request_mock)

        settings_client.perform_request('GET')
        settings_client.perform_request('PATCH', data=patch_data)

        assert get_perform_request_mock.called
        assert patch_perform_request_mock.called
        patch_perform_request_mock.assert_called_with(data=patch_data)
