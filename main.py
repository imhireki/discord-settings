import time
import json

from iter import iterator, iterable
from settings import settings
from api import client


data_emoji = {
    'moon': ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔'],
    'weather': ['🌤', '⛅', '🌥', '☁', '🌦', '🌧', '⛈'],
    'star': ['💫', '✨', '⭐', '🌟' ],
    'skull': ['💀', '☠️'],
}

data_text = {
    'sleep': ['zzzzz'],
    'o': ['oooooooooo'],
}

if __name__ == '__main__':
    JWT = ''

    request_client = client.RequestClientV9(JWT)
    _previous_settings = request_client.get()

    local_settings = settings.LocalSettings(request_client)

    iterable_emoji = iterable.EmojiName(data_emoji['moon'])
    iterable_status = iterable.Status()
    iterable_text = iterable.Text(['woooah'])

    iterator_text = iterator.Increase(iterable.Text(['$_', '$ ']))
    # iterator_text = iterator.IteratorManager(
    #     iterator.UpperIndexItem(iter(iterable_text)),
    #     iterator.Increase(["$"]),
    #     iterator.Increase(["_", " "])
    #     )

    buffer = settings.SettingsBuffer(iter(iterable_emoji),
                                     iter(iterable_status),
                                     iterator_text)

    try:
        while True:
            updated_buffer = buffer.get_updated_buffer()
            local_settings.update(updated_buffer)
            time.sleep(3)
    except Exception:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        request_client.patch(json.loads(_previous_settings.text))
