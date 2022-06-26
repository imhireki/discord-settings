from api import client

from settings import settings

from iterators import iterator
from iterables import iterable

from polls import poll


data_emoji = {
    'moon': ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔'],
    'star': ['💫', '✨', '⭐', '🌟' ],
    'weather': ['🌤', '⛅', '🌥', '☁', '🌦', '🌧', '⛈'],
}

data_text = {
    'laugh': ['bahaha', 'lol'],
}


if __name__ == '__main__':
    JWT = ''

    request_client = client.RequestClientV9(JWT)

    _settings = settings.LocalSettings(request_client)
    _settings.update({'status': 'online'})

    # Iterable
    emoji_name = iterable.EmojiName(data_emoji['star'])
    text = iterable.Text(data_text['laugh'])
    status = iterable.Status()

    # Iterator
    iter_emoji_name = iter(emoji_name)
    iter_status = iter(status)

    iter_prefix = iterator.Increase(["$"])
    _iter_text = iterator.ItemsBeforeNextIndex(iter(text))
    iter_suffix = iterator.Increase(["_", " "])

    iter_text = iterator.IteratorManager(_iter_text, iter_prefix, iter_suffix)

    # Buffer
    buffer = settings.SettingsBuffer(iter_emoji_name, iter_text, iter_status)

    try:
        # Polling
        poll.Poll(_settings, buffer).polling(timeout=3)
    except Exception:
        pass
    finally:
        request_client.patch({
            'custom_status': None,
            'status': 'dnd'
        })
