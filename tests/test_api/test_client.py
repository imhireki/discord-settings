import json

import pytest

from api import client


class TestRequestClientV9:
    def test_get(self, mocker, auth_token):
        request_mock = mocker.patch('requests.get')

        request_client = client.RequestClientV9(auth_token)
        response = request_client.get()

        assert response.status_code == request_mock.return_value.status_code
        assert response.text == request_mock.return_value.text
        assert request_mock.call_args.args[0] == request_client._endpoint
        assert (request_mock.call_args.kwargs['headers']
                == request_client._request_manager._requests['GET'].
                   _request_method._headers)

    def test_patch(self, mocker, auth_token):
        data = {'data': 123}
        request_mock = mocker.patch(
            'requests.patch',
            return_value=mocker.Mock(text=json.dumps(data)))

        request_client = client.RequestClientV9(auth_token)
        response = request_client.patch(data)

        assert response.status_code == request_mock.return_value.status_code
        assert data == json.loads(response.text)
        assert request_mock.call_args.args[0] == request_client._endpoint
        assert (request_mock.call_args.kwargs['headers']
                == request_client._request_manager._requests['PATCH'].
                   _request_method._headers)
