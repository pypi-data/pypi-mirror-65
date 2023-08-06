from micro_toolkit.data_process.batch_iterator import BatchingIterator


def test_batch_iterator_from_list():
    data = list(range(19))

    result = []

    bi = BatchingIterator(5)
    for i in bi(data):
        result.append(i)

    assert result == [
        [0, 1, 2, 3, 4],
        [5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14],
        [15, 16, 17, 18],
    ]


def test_batch_iterator_from_dict():
    data = {"apple": list(range(0, 19)), "banana": list(range(1, 20))}

    result = []

    bi = BatchingIterator(5)
    for i in bi(data):
        result.append(i)

    expected = [
        {"apple": [0, 1, 2, 3, 4, 5], "banana": [1, 2, 3, 4, 5, 6]},
        {"apple": [6, 7, 8, 9, 10], "banana": [7, 8, 9, 10, 11]},
        {"apple": [11, 12, 13, 14, 15], "banana": [12, 13, 14, 15, 16]},
        {"apple": [16, 17, 18], "banana": [17, 18, 19]},
    ]

    assert result == expected


if __name__ == "__main__":
    test_batch_iterator_from_dict()
