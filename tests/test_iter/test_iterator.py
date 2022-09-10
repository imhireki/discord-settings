from iter import iterator


def test_increase(make_setting_iterable, request_data_value, items):
    increase_iterator = iterator.Increase(make_setting_iterable('x', items))

    request_data = increase_iterator.get_request_data(request_data_value)
    next_0 = next(increase_iterator)
    next_1 = next(increase_iterator)
    next_2 = next(increase_iterator)

    assert request_data == {"setting": {"x": request_data_value}}
    assert next_0 == items[0]
    assert next_1 == items[1]
    assert next_2 == items[0]

def test_decrease(make_setting_iterable, request_data_value, items):
    decrease_iterator = iterator.Decrease(make_setting_iterable('x', items))

    request_data = decrease_iterator.get_request_data(request_data_value)
    next_0 = next(decrease_iterator)
    next_1 = next(decrease_iterator)
    next_2 = next(decrease_iterator)

    assert request_data == {"setting": {"x": request_data_value}}
    assert next_0 == items[1]
    assert next_1 == items[0]
    assert next_2 == items[1]

def test_single_item(make_iterator, items):
    iterator_mock = make_iterator(items)

    single_item_iterator = iterator.SingleItem(iterator_mock)
    next_0 = next(single_item_iterator)
    next_1 = next(single_item_iterator)
    next_2 = next(single_item_iterator)

    assert next_0 == items[0][0]
    assert next_1 == items[0][1]
    assert next_2 == items[1][0]

def test_items_before_next_index(make_iterator, items):
    iterator_mock = make_iterator(items)

    items_before_next_index_iterator = iterator.ItemsBeforeNextIndex(
        iterator_mock)
    next_0 = next(items_before_next_index_iterator)
    next_1 = next(items_before_next_index_iterator)
    next_2 = next(items_before_next_index_iterator)

    assert next_0 == items[0][:1]
    assert next_1 == items[0][:2]
    assert next_2 == items[1][:1]

def test_items_after_index(make_iterator, items):
    iterator_mock = make_iterator(items)

    items_after_index_iterator = iterator.ItemsAfterIndex(iterator_mock)
    next_0 = next(items_after_index_iterator)
    next_1 = next(items_after_index_iterator)
    next_2 = next(items_after_index_iterator)

    assert next_0 == items[0][-1:]
    assert next_1 == items[0][-2:]
    assert next_2 == items[1][-1:]

def test_upper_index_item(make_iterator, items, make_upper_on_collection):
    iterator_mock = make_iterator(items)

    upper_index_item_iterator = iterator.UpperIndexItem(iterator_mock)
    next_0 = next(upper_index_item_iterator)
    next_1 = next(upper_index_item_iterator)
    next_2 = next(upper_index_item_iterator)

    assert next_0 == make_upper_on_collection(0, items[0])
    assert next_1 == make_upper_on_collection(1, items[0])
    assert next_2 == make_upper_on_collection(0, items[1])

def test_iterator_manager(make_iterator, items):
    prefix_iterator = iter(items[1])
    iterator_mock = make_iterator(items)
    suffix_iterator = iter(items[1])

    iterator_manager = iterator.IteratorManager(
        iterator_mock, prefix_iterator, suffix_iterator)
    next_0 = next(iterator_manager)
    next_1 = next(iterator_manager)

    assert next_0 == items[1][0] + items[0] + items[1][0]
    assert next_1 == items[1][1] + items[1] + items[1][1]
