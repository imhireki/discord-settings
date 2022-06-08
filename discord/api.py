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
