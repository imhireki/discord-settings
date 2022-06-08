import pytest

from discord.api import *


class TestGet:
    def test_perform_get_request(self, mocker, requests_mock,auth_token):
        # ARRANGE
        url, text_data = 'http://test.com/', '{"test": 123}'
        headers = {'Authorization': auth_token}  # GetHeaders.headers
        request_method = Get(url=url, headers=headers)

        # MOCK
        requests_mock.get(url, text=text_data)

        # ACT
        response = request_method.perform_get_request()

        # ASSERT
        assert request_method.headers['Authorization']
        assert response.status_code == 200
        assert response.url == url
        assert response.text == text_data

