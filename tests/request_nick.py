import requests
from time import sleep


if __name__ == '__main__':
    STOMP_NICK_URL = 'https://discord.com/api/v9/guilds/'\
                     '864252583584464956/members/@me'

    JWT = '' 

    request_headers = {
        'Content-Type': 'application/json',
        'authorization': JWT,
        } 

    emojis = ['👍','👆', '🤟', '🤘', '🤙']
     
    nicks = [
        'Hireki ' + emoji
        for emoji in emojis
        ]

    # c = 0
    while True:
        for nick in nicks:

            data = {
                'nick': nick,
                }

            request = requests.patch(
                STOMP_NICK_URL,
                json=data,
                headers=request_headers
                ) 

            sleep(15)

            # if c > 20:
            #   sleep(300)
            #  c = 0 
            
