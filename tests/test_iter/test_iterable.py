import pytest

from iter import iterable


emojis = ['💫', '✨', '⭐']
text_list = ['x', 'y', 'z']


@pytest.mark.parametrize('setting', [
    iterable.EmojiName(emojis),
    iterable.Text(text_list),
    iterable.Status()
])
def test_iterators(mocker, setting):
    increase_iterator_mock = mocker.patch('iter.iterator.Increase')
    decrease_iterator_mock = mocker.patch('iter.iterator.Decrease')

    iter(setting)
    setting.decrease()

    assert increase_iterator_mock.call_args.args[0] == setting
    assert decrease_iterator_mock.call_args.args[0] == setting

def test_emoji_name_setting():
    emoji_name_iterable = iterable.EmojiName(emojis)

    request_data_0 = emoji_name_iterable.get_request_data(emojis[0])
    request_data_1 = emoji_name_iterable.get_request_data(emojis[1])
    request_data_2 = emoji_name_iterable.get_request_data(emojis[2])

    assert request_data_0 == {"custom_status": {"emoji_name": emojis[0]}}
    assert request_data_1 == {"custom_status": {"emoji_name": emojis[1]}}
    assert request_data_2 == {"custom_status": {"emoji_name": emojis[2]}}

def test_text():
    text = iterable.Text(text_list)

    request_data_0 = text.get_request_data(text_list[0])
    request_data_1 = text.get_request_data(text_list[1])
    request_data_2 = text.get_request_data(text_list[2])

    assert request_data_0 == {"custom_status": {"text": text_list[0]}}
    assert request_data_1 == {"custom_status": {"text": text_list[1]}}
    assert request_data_2 == {"custom_status": {"text": text_list[2]}}

def test_status():
    status = iterable.Status()

    request_data_0 = status.get_request_data(status.items[0])
    request_data_1 = status.get_request_data(status.items[1])
    request_data_2 = status.get_request_data(status.items[2])

    assert request_data_0 == {"status": status.items[0]}
    assert request_data_1 == {"status": status.items[1]}
    assert request_data_2 == {"status": status.items[2]}
