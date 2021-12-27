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

    def perform_action(self, text_list, emoji_list, status_list):
        # Set iterators
        self.it_status_list = iter(status_list)
        self.it_emoji_list = iter(emoji_list)
        self.it_text_list  = iter(text_list)

        while True:
            data = {
                "custom_status": {
                    "emoji_name": self.get_next_emoji(emoji_list),
                    "text": self.get_next_word(text_list)
                },
                "status": self.get_next_status(status_list)
            }

            self.perform_request(data)

    def get_next_word(self, text_list):
        try:
            return self.it_text_list.__next__()
        except StopIteration:
            self.it_text_list = iter(text_list)
            return self.it_text_list.__next__()

    def get_next_emoji(self, emoji_list):
        try:
            return self.it_emoji_list.__next__()
        except StopIteration:
            self.it_emoji_list = iter(emoji_list)
            return self.it_emoji_list.__next__()

    def get_next_status(self, status_list):
        try:
            return self.it_status_list.__next__()
        except StopIteration:
            self.it_status_list = iter(status_list)
            return self.it_status_list.__next__()

    def perform_request(self, data):
        requests.patch(url=self.endpoint,
                       headers=self.headers,
                       json=data)
        sleep(4)

if __name__ == '__main__':
    JWT = ''
    ds = DiscordStatus(JWT)

    to_emoji = ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔']
    to_text = [f'{i} hm' for i in range(100, 0, -1)]
    #to_emoji = ['✨', '💫', '⭐️', '🌟']

    to_status = ['online', 'idle', 'dnd']

    ds.perform_action(text_list=to_text,
                      emoji_list=to_emoji,
                      status_list=to_status)
