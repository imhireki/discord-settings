from abc import ABC, abstractmethod
from typing import Union, Any

import requests

from . import header


class IRequestMethod(ABC):
    def __init__(self, url: str, headers: dict[str, str]) -> None:
        self.url: str = url
        self.headers: dict[str, str] = headers


class Get(IRequestMethod):
    def get(self) -> requests.Response:
        return requests.get(self.url, headers=self.headers)


class Patch(IRequestMethod):
    def patch(self, data: dict[str, Any]) -> requests.Response:
        return requests.patch(self.url, headers=self.headers, json=data)


class IRequest(ABC):
    def __init__(self, request_method: IRequestMethod) -> None:
        self.request_method: IRequestMethod = request_method

    @abstractmethod
    def perform_request(self, *args, **kwargs) -> requests.Response: pass


class PatchRequest(IRequest):
    def perform_request(self, *args, **kwargs) -> requests.Response:
        return self.request_method.patch(*args, **kwargs)


class GetRequest(IRequest):
    def perform_request(self, *args, **kwargs) -> requests.Response:
        return self.request_method.get(*args, **kwargs)


class RequestManager:
    def __init__(self) -> None:
        self._requests: dict[str, IRequest] = {}

    def add_request(self, request_name: str, request: IRequest) -> None:
        self._requests[request_name] = request

    def perform_request(self, request_name: str, *args, **kwargs) -> requests.Response:
        return self._requests[request_name].perform_request(*args, **kwargs)
