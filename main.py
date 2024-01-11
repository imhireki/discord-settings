import json
import time

from settings import DiscordSettings, SettingsBuffer
from api.client import RequestClientV9
from iter import iterator, iterable


emoji = iterable.EmojiName(['🌑', '🌘', '🌗', '🌖', '🌕', '🌔', '🌓', '🌒'])
status = iterable.Status(['idle', 'dnd'])
text = iterable.Text(['zzzzz'])

iterator_text = iterator.IteratorManager(
    iterator.UpperIndexItem(iter(text)),
    iterator.Increase(['$']),
    iterator.Increase([' ', '_'])
)

settings_buffer = SettingsBuffer(iter(emoji), iter(status), iterator_text)

JWT = ''
request_client = RequestClientV9(JWT)

settings_backup = json.loads(request_client.get().text)

discord_settings = DiscordSettings(request_client)

try:
    while True:
        updated_buffer = settings_buffer.get_updated_buffer()
        print(updated_buffer)
        # discord_settings.update(updated_buffer)
        time.sleep(1)
except KeyboardInterrupt: pass
# except Exception: pass
finally:
    request_client.patch(settings_backup)

