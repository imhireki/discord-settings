import pytest

from iter import iterable, iterator


@pytest.fixture
def auth_token() -> str:
    return 'eyJCI6IkpCJ9.eJzWiOiMyfQ.SfMyV_assw5c'

@pytest.fixture
def request_data_value():
    return '123'

@pytest.fixture
def items():
    return ["xy", "ab"]

@pytest.fixture
def make_upper_on_collection():
    return lambda index, collection: ''.join([
        item.upper() if index == item_index else item
        for item_index, item in enumerate(collection)
    ])

@pytest.fixture
def iterator_mock(iterable_mock):
    class Iterator(iterator.IUnlimitedItems):
        """[abc, xyz]  =  abc -> xyz"""
        def _get_collection_item(self) -> str:
            return self._collection[self._collection_index]

        def _set_next_collection_index(self) -> None:
            if not hasattr(self, '_collection_index'):
                return self._reset_collection_index()
            self._collection_index += 1

        def _reset_collection_index(self) -> None:
            self._collection_index = 0
    return Iterator(iterable_mock)

@pytest.fixture
def make_iterator():
    def _make_iterator(iterable):
        class Iterator(iterator.IUnlimitedItems):
            """[abc, xyz]  =  abc -> xyz"""
            def _get_collection_item(self) -> str:
                return self._collection[self._collection_index]

            def _set_next_collection_index(self) -> None:
                if not hasattr(self, '_collection_index'):
                    return self._reset_collection_index()
                self._collection_index += 1

            def _reset_collection_index(self) -> None:
                self._collection_index = 0
        return Iterator(iterable)
    return _make_iterator

@pytest.fixture
def make_setting_iterable():
    def _make_setting_iterable(id: str,
                               items: list) -> iterable.ISettingIterable:
        class Setting(iterable.ISettingIterable):
            def __init__(self) -> None:
                super().__init__(items)

            def get_request_data(self, value: str) -> dict:
                return {"setting": {id: value}}
        return Setting()
    return _make_setting_iterable
