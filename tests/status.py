#!/bin/python3

import requests
from time import sleep


class DiscordStatus:
    def __init__(self, JWT):
        self.headers = JWT
        self.endpoint = 'https://discord.com/api/v9/users/@me/settings'

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = {'Content-Type': 'application/json',
                         'Authorization': value}


    def perform_action_1(self, items:list):
        while True:
            for _ in items:
                self.perform_request(_)

    def perform_request(self, value):
        requests.patch(url=self.endpoint,
                       headers=self.headers,
                       json=self.get_data(value))
        sleep(1)

    @staticmethod
    def get_data(value):
        return {"custom_status": {"text": f"{value}"}}


if __name__ == '__main__':
    JWT = ''
    ds = DiscordStatus(JWT)

    items = ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔']
    ds.perform_action_1(items)
