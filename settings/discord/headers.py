from typing import Dict


class IRequestHeaders:
    """Interface for HTTP request's headers"""

    _headers: Dict[str, str] = {}

    @property
    def headers(self):
        return self._headers

    @property
    def authorization(self):
        return self._authorization

    @authorization.setter
    def authorization(self, JWT: str):
        self._authorization = {'Authorization': JWT}
        self.headers.update(self.authorization)


class PatchRequestHeaders(IRequestHeaders):
    """Set the headers for PATCH requests."""

    _json_content_type = 'application/json'

    def __init__(self, JWT: str):
        self.authorization = JWT
        self.content_type = self._json_content_type

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, content_type: str):
        self._content_type = {'Content-Type': content_type}
        self.headers.update(self.content_type)


class GetRequestHeaders(IRequestHeaders):
    """Set the headers for GET requests."""

    def __init__(self, JWT: str):
        self.authorization = JWT
