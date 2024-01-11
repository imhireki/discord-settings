from typing import Any, Type
from abc import ABC

import requests

from api import header, request


class IRequestClient(ABC):
    _request_manager: request.RequestManager
    _endpoint: str
    _auth_token: str

    def add_request_to_manager(
            self, request_name: str,
            request: Type[request.IRequest],
            request_method: Type[request.IRequestMethod],
            request_headers: Type[header.IRequestHeaders]) -> None:

        headers = request_headers(self._auth_token).as_dict()
        method = request_method(self._endpoint, headers)
        _request = request(method)
        self._request_manager.add_request(request_name, _request)


class RequestClientV9(IRequestClient):
    _endpoint: str = 'https://discord.com/api/v9/users/@me/settings'

    def __init__(self, auth_token: str) -> None:
        self._auth_token: str = auth_token
        self._request_manager = request.RequestManager()

        self.add_request_to_manager('GET', request.GetRequest,
                                    request.Get, header.Get)
        self.add_request_to_manager('PATCH', request.PatchRequest,
                                    request.Patch, header.Patch)

    def get(self) -> requests.Response:
        return self._request_manager.perform_request('GET')

    def patch(self, data: dict[str, Any]) -> requests.Response:
        return self._request_manager.perform_request('PATCH', data)
