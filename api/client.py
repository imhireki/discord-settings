from abc import ABC, abstractmethod
from typing import Union, Any

import requests

from . import header
from . import request


class IRequestClient(ABC):
    endpoint: str
    auth_token: str

    def add_request_to_manager(self, request_name: str, request: request.IRequest,
                               request_method: request.IRequestMethod,
                               request_headers: header.IRequestHeaders) -> None:

        headers = request_headers(self.auth_token).headers
        method = request_method(self.endpoint, headers)
        _request = request(method)
        self.request_manager.add_request(request_name, _request)


class RequestClientV9(IRequestClient):
    endpoint = 'https://discord.com/api/v9/users/@me/settings'

    def __init__(self, auth_token: str) -> None:
        self.auth_token: str = auth_token
        self.request_manager: request.RequestManager = request.RequestManager()

        self.add_request_to_manager('GET', request.GetRequest, request.Get, header.Get)
        self.add_request_to_manager('PATCH', request.PatchRequest, request.Patch, header.Patch)

    def get(self) -> requests.Response:
        return self.request_manager.perform_request('GET')

    def patch(self, data: dict[str, Any]) -> requests.Response:
        return self.request_manager.perform_request('PATCH', data)
