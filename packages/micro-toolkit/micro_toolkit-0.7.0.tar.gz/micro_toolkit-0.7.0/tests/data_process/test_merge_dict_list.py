from micro_toolkit.data_process.merge_dict_list import merge_dict_list


def test_mrege_dict_list():
    # dictionaries with non-equal keys, values all lists for simplicity
    one = {"a": [1, 2], "c": [5, 6]}
    two = {"d": [7, 8]}
    three = {"a": [3], "b": [4]}

    result = merge_dict_list(one, two, three)

    expected = {"a": [1, 2, 3], "b": [4], "c": [5, 6], "d": [7, 8]}

    assert result == expected
