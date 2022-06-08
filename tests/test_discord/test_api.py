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
        request_method_mock = mocker.Mock(
            perform_patch_request=perform_patch_request_mock
        )

        patch_request = PatchRequest(request_method_mock)

        patch_request.perform_request()

        assert perform_patch_request_mock.called

