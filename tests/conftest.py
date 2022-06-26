import pytest


@pytest.fixture
def auth_token() -> str:
    return 'eyJCI6IkpCJ9.eJzWiOiMyfQ.SfMyV_assw5c'

@pytest.fixture
def iterable_items():
    return ["xyz", "abc"]

@pytest.fixture
def iterable_mock(mocker, iterable_items):
    def get_request_data(value):
        return {"test": value}
    return mocker.Mock(items=iterable_items, get_request_data=get_request_data)

@pytest.fixture
def request_data_value():
    return '123'

@pytest.fixture
def iterator_mock(iterable_mock):
    class Iterator:
        def __init__(self) -> None:
            self.iterable = iterable_mock
            self.collection = self.set_collection(self.iterable)
            self.max_collection_index: int = len(self.collection) - 1

        def set_collection(self, iterable):
            return iterable if isinstance(iterable, (list, tuple)) else iterable.items

        def get_request_data(self, value: str) -> dict[str, str]:
            return self.iterable.get_request_data(value)

        def indexes_in_collection_range(self, index: int, max_index: int) -> bool:
            return True if 0 <= index <= max_index else False

        def __next__(self) -> str:
            self.set_next_collection_index()

            if not self.indexes_in_collection_range(self.collection_index,
                                                    self.max_collection_index):
                self.reset_collection_index()

            return self.get_collection_item()

        def get_collection_item(self) -> str:
            return self.collection[self.collection_index]

        def set_next_collection_index(self) -> None:
            if not hasattr(self, 'collection_index'):
                return self.reset_collection_index()
            self.collection_index += 1

        def reset_collection_index(self) -> None:
            self.collection_index = 0

    return Iterator
