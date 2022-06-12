from abc import ABC, abstractmethod


class IRequestHeaders(ABC):
    def __init__(self, auth_token: str) -> None:
        self.headers: dict[str, str] = {}
        self.populate_headers(auth_token)

    @abstractmethod
    def populate_headers(self, auth_token: str) -> None: pass


class Patch(IRequestHeaders):
    def populate_headers(self, auth_token: str) -> None:
        self.headers.update({
            'Authorization': auth_token, 'Content-Type': 'application/json'
        })


class Get(IRequestHeaders):
    def populate_headers(self, auth_token: str) -> None:
        self.headers.update({'Authorization': auth_token})
