from discord import api, headers
from iterators import iterator
from iterables import iterable
from state import state
from polls import poll


data_emoji = {
    'moon': ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔'],
    'star': ['💫', '✨', '⭐', '🌟' ],
    'weather': ['🌤', '⛅', '🌥', '☁', '🌦', '🌧', '⛈'],
}

data_text = {
    'laugh': ['Bahaha'],
}


if __name__ == '__main__':
    JWT = ''

    api = api.DiscordSettingsAPI(JWT)  # Request

    settings = state.Settings(api)  # Settings

    # Iterable
    emoji_name = iterable.EmojiName(data_emoji['star'])
    text = iterable.Text(data_text['laugh'])
    status = iterable.Status()

    # Iterator
    iter_emoji_name = iter(emoji_name)
    iter_status = iter(status)
    iter_text = text.multiple_before_index()

    # Iterators' Decorators
    iter_text = iterator.Prefix(iter_text, '$')
    iter_text = iterator.Suffix(iter_text, '_ ')

    # Buffer
    buffer = state.Buffer(
        iterables=[emoji_name, text, status],
        iterators=[iter_emoji_name, iter_text, iter_status]
    )

    try:
        # Polling
        poll.Poll(settings, buffer).polling(timeout=1)
    except Exception:
        pass
    finally:
        api.patch({
            'custom_status': None,
            'status': 'dnd'
        })
