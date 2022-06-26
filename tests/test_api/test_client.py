import pytest

from api import client


def dict_items_in_dict(dict_a: dict, dict_b: dict):
    match_items = dict([
        a
        for a in dict_a.items()
        for b in dict_b.items()
        if a == b
    ])
    return True if match_items == dict_a else False

def test_client_get_request(requests_mock, auth_token):
    request_client = client.RequestClientV9(auth_token)

    _get_request = request_client.request_manager._requests['GET']
    get_headers = _get_request.request_method.headers

    text_data = '{"test": 123}'
    requests_mock.get(request_client.endpoint, text=text_data)

    response = request_client.get()

    assert response.status_code == 200
    assert response.url == request_client.endpoint
    assert response.text == text_data
    assert dict_items_in_dict(get_headers, response.request.headers)

def test_client_patch_request(requests_mock, auth_token):
    request_client = client.RequestClientV9(auth_token)

    _patch_request = request_client.request_manager._requests['PATCH']
    patch_headers = _patch_request.request_method.headers

    data = {'data': 123}
    requests_mock.patch(request_client.endpoint, json=data)

    response = request_client.patch(data)

    assert response.status_code == 200
    assert response.url == request_client.endpoint
    assert eval(response.text) == data
    assert dict_items_in_dict(patch_headers, response.request.headers)

