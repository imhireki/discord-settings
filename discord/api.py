from abc import ABC, abstractmethod
from typing import Dict, Union

import requests

from . import headers


class IRequestMethod(ABC):
    def __init__(self, url: str, headers: Dict[str, str]) -> None:
        self.url: str = url
        self.headers: Dict[str, str] = headers


class Get(IRequestMethod):
    def perform_get_request(self) -> requests.Response:
        return requests.get(self.url, headers=self.headers)


class Patch(IRequestMethod):
    def perform_patch_request(self, data: Dict[str, Union[str, None]],
                              ) -> requests.Response:
        return requests.patch(self.url, headers=self.headers, json=data)


class IRequest(ABC):
    def __init__(self, request_method: IRequestMethod):
        self.request_method: IRequestMethod = request_method

    @abstractmethod
    def perform_request(self, *args, **kwargs): pass


class PatchRequest(IRequest):
    def perform_request(self, *args, **kwargs) -> requests.Response:
        return self.request_method.perform_patch_request(*args, **kwargs)


class GetRequest(IRequest):
    def perform_request(self, *args, **kwargs) -> requests.Response:
        return self.request_method.perform_get_request(*args, **kwargs)


class DiscordSettingsRequestClient:
    ENDPOINT = 'https://discord.com/api/v9/users/@me/settings'
    _requests: Dict[str, IRequest] = {}

    def set_request(self, request_name: str, request: IRequest) -> None:
        self._requests[request_name] = request

    def perform_request(self, request_name: str,
                        *args, **kwargs) -> requests.Response:
        return self._requests[request_name].perform_request(*args, **kwargs)
