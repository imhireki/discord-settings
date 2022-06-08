from typing import Dict
from abc import ABC, abstractmethod


class IRequestHeader(ABC):
    def __init__(self, header: str):
        self.header: str = header

    @property
    @abstractmethod
    def header_key(self) -> str: pass

    @property
    def header(self) -> Dict[str, str]:
        return self._header

    @header.setter
    def header(self, header: str):
        self._header = {self.header_key: header}


class Authorization(IRequestHeader):
    @property
    def header_key(self) -> str:
        return 'Authorization'


class ContentType(IRequestHeader):
    @property
    def header_key(self) -> str:
        return 'Content-Type'


class IRequestMethodHeaders(ABC):
    _headers: Dict[str, str] = {}

    def __init__(self, auth_token: str) -> None:
        self.auth_token: str = auth_token
        self.populate_headers()

    @property
    def headers(self) -> Dict[str, str]:
        return self._headers

    @abstractmethod
    def populate_headers(self) -> None: pass


class PatchHeaders(IRequestMethodHeaders):
    def populate_headers(self) -> None:
        authorization = Authorization(self.auth_token)
        self.headers.update(authorization.header)

        content_type = ContentType('application/json')
        self.headers.update(content_type.header)


class GetHeaders(IRequestMethodHeaders):
    def populate_headers(self) -> None:
        authorization = Authorization(self.auth_token)
        self.headers.update(authorization.header)
