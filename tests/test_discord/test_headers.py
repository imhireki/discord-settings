import pytest
from discord.headers import *


class TestRequestHeader:
    def test_authorization_request_header(self, auth_token):
        expected_value = {'Authorization': auth_token}
        authorization = AuthorizationRequestHeader(auth_token)

        authorization_header = authorization.header

        assert authorization_header == expected_value

    def test_content_type_request_header(self):
        content_type = 'application/json'
        expected_value = {'Content-Type': content_type}
        content_type = ContentTypeRequestHeader(content_type)

        content_type_header = content_type.header

        assert content_type_header == expected_value


class TestRequestMethodHeaders:
    def test_get_request_method_headers(self, auth_token):
        expected_value = dict(Authorization=auth_token)

        get_request_method_headers = GetRequestMethodHeaders(auth_token)

        assert get_request_method_headers.headers == expected_value

    def test_patch_request_method_headers(self, auth_token):
        expected_value = {
            'Authorization': auth_token,
            'Content-Type': 'application/json'
        }
        patch_request_method_headers = PatchRequestMethodHeaders(auth_token)

        assert patch_request_method_headers.headers == expected_value
