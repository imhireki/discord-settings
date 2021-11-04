import requests
from time import sleep


if __name__ == '__main__':
    urls = [] 

    JWT = '' 

    request_headers = {
        'Content-Type': 'application/json',
        'authorization': JWT,
        'Content-Length': '0',
        } 

    previous = None
    while True:
        for url in urls:
            request = requests.put(
                url,
                headers=request_headers
                ) 
            sleep(0.5)
            if previous:
                request2 = requests.delete(
                    previous, headers=request_headers
                    )
            previous = url
            sleep(1)

