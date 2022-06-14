from iterables import iterable
import pytest


emojis = ["💫", "🌟"]
text_list = ["x", "y", "z"]

@pytest.mark.parametrize('setting', [
    iterable.EmojiName(emojis),
    iterable.Text(text_list),
    iterable.Status()
])
def test_default_iterator(mocker, setting):
    iterator_mock = mocker.patch('iterators.iterator.Unlimited')
    iter(setting)
    iterator_mock.assert_called_with(setting._items)

def test_emoji_name_setting():
    emoji_name_iterable = iterable.EmojiName(emojis)

    for emoji in emojis:
        expected_data = {"custom_status": {"emoji_name": emoji}}
        assert emoji_name_iterable.get_request_data(emoji) == expected_data

def test_text_setting(mocker):
    text_iterable = iterable.Text(text_list)
    data_before_index_mock = mocker.patch('iterators.iterator.MultipleBeforeIndex')

    text_iterable.iter_data_before_index()

    for text in text_list:
        expected_data = {"custom_status": {"text": text}}
        assert text_iterable.get_request_data(text) == expected_data

    data_before_index_mock.assert_called_with(text_list)

def test_status_setting():
    status_iterable = iterable.Status()

    for status in status_iterable._items:
        expected_data = {"status": status}
        assert status_iterable.get_request_data(status) == expected_data
