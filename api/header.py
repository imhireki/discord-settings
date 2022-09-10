from abc import ABC, abstractmethod


class IRequestHeaders(ABC):
    def __init__(self, auth_token: str) -> None:
        self._headers: dict[str, str] = {}
        self._populate_headers(auth_token)

    @abstractmethod
    def _populate_headers(self, auth_token: str) -> None: pass

    def as_dict(self) -> dict[str, str]:
        return self._headers


class Patch(IRequestHeaders):
    def _populate_headers(self, auth_token: str) -> None:
        self._headers.update({
            'Authorization': auth_token,
            'Content-Type': 'application/json'
            })


class Get(IRequestHeaders):
    def _populate_headers(self, auth_token: str) -> None:
        self._headers.update({'Authorization': auth_token})
