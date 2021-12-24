#! /usr/bin/python3

import requests
from time import sleep


class RainbowPuke:
    def __init__(self, JWT, urls, timeouts):
        self.timeouts = timeouts
        self.urls = urls
        self.headers = JWT

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = {'Content-Type': 'application/json',
                         'authorization': value,
                         'Content-Length': '0'}

    def perform_color_change(self):
        prev_url = None

        while True:
            for url in self.urls:
                self.add_color(url)

                if prev_url:
                    self.rem_color(prev_url)

                prev_url = url

    def add_color(self, url):
        requests.put(url,
                     headers=self.headers)

        sleep(self.timeouts['PUT']) # timeout pos PUT

    def rem_color(self, url):
        requests.delete(url,
                        headers=self.headers)

        sleep(self.timeouts['DELETE']) # timeout pos DELETE


if __name__ == '__main__':
    JWT = ''
    urls = []
    timeouts = {}

    rp = RainbowPuke(JWT, urls, timeouts)
    rp.perform_color_change()
