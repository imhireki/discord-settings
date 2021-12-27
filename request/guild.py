#!/bin/python3

import requests
from time import sleep
import random


class RainbowPuke:
    """ Manage the change of the username color """
    def __init__(self, JWT:str, urls:list, timeouts:dict):
        self.timeouts = timeouts
        self.urls = urls
        self.headers = JWT

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        """ Request's headers made out of the JWT token """
        self._headers = {'Content-Type': 'application/json',
                         'authorization': value,
                         'Content-Length': '0'}

    def perform_color_change(self):
        """ Loop between the urls to change the username color """
        prev_url = None

        while True:
            for url in self.urls:
                self.add_color(url)

                if prev_url:
                    self.rem_color(prev_url)

                prev_url = url

    def add_color(self, url):
        """ Perform a request(PUT) to add a color """
        requests.put(url,
                     headers=self.headers)

        sleep(self.timeouts['PUT']) # timeout pos PUT

    def rem_color(self, url):
        """ Perform a request(DELETE) to remove a color """
        requests.delete(url,
                        headers=self.headers)

        sleep(self.timeouts['DELETE']) # timeout pos DELETE


if __name__ == '__main__':
    JWT = ''

    urls = [
        'https://discord.com/api/v9/channels/793239305811263511/'\
        'messages/793241061442977812/reactions/'\
        f'{x}%EF%B8%8F%E2%83%A3/@me'
        for x in range(9)
    ]

    random.shuffle(urls)

    timeouts = {'PUT': 2,
                'DELETE':2}

    rp = RainbowPuke(JWT, urls, timeouts)
    rp.perform_color_change()
