from abc import ABC, abstractmethod
from typing import Dict, Union

import requests

from . import headers


class IRequestMethod(ABC):
    def __init__(self, url: str, headers: Dict[str, str]) -> None:
        self.url: str = url
        self.headers: Dict[str, str] = headers


class Get(IRequestMethod):
    def perform_get_request(self) -> Dict[str, Union[str, None]]:
        return requests.get(self.url, headers=self.headers)


class Patch(IRequestMethod):
    def perform_patch_request(self, data: Dict[str, Union[str, None]]) -> None:
        return requests.patch(self.url, headers=self.headers, json=data)


class IRequest(ABC):
    def __init__(self, request_method: IRequestMethod):
        self.request_method = request_method

    @abstractmethod
    def perform_request(self): pass


class PatchRequest(IRequest):
    def perform_request(self) -> None:
        return self.request_method.perform_patch_request()
