import pytest

from iterables import iterable


emojis = ['💫', '✨', '⭐']
text_list = ['x', 'y', 'z']

@pytest.mark.parametrize('setting', [
    iterable.EmojiName(emojis),
    iterable.Text(text_list),
    iterable.Status()
])
def test_iterators(mocker, setting):
    increase_iterator_mock = mocker.patch('iterators.iterator.Increase')
    decrease_iterator_mock = mocker.patch('iterators.iterator.Decrease')

    iter(setting)
    setting.decrease()

    increase_iterator_mock.assert_called_with(setting)
    decrease_iterator_mock.assert_called_with(setting)

def test_emoji_name_setting():
    emoji_name_iterable = iterable.EmojiName(emojis)

    for emoji in emojis:
        expected_data = {"custom_status": {"emoji_name": emoji}}
        assert emoji_name_iterable.get_request_data(emoji) == expected_data

def test_text_setting():
    text_iterable = iterable.Text(text_list)

    for text in text_list:
        expected_data = {"custom_status": {"text": text}}
        assert text_iterable.get_request_data(text) == expected_data

def test_status_setting():
    status_iterable = iterable.Status()

    for status in status_iterable.items:
        expected_data = {"status": status}
        assert status_iterable.get_request_data(status) == expected_data
