import pytest
from discord.headers import *


class TestRequestHeader:
    def test_authorization_request_header(self, auth_token):
        expected_value = {'Authorization': auth_token}
        authorization_header = Authorization(auth_token).header

        assert authorization_header == expected_value

    def test_content_type_request_header(self):
        content_type = 'application/json'

        expected_value = {'Content-Type': content_type}
        content_type_header = ContentType(content_type).header

        assert content_type_header == expected_value


class TestRequestMethodHeaders:
    def test_get_headers(self, auth_token):
        expected_value = dict(Authorization=auth_token)
        get_headers = GetHeaders(auth_token).headers

        assert get_headers == expected_value

    def test_patch_headers(self, auth_token):
        expected_value = {
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        }
        patch_headers = PatchHeaders(auth_token).headers

        assert patch_headers == expected_value
