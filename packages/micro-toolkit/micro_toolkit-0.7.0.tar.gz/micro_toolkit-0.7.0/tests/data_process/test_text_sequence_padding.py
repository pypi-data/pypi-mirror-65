from micro_toolkit.data_process.text_sequence_padding import TextSequencePadding


def test_text_sequence_padding():
    tsp = TextSequencePadding("0")

    input_data = [
        ['1', '2', '3'],
        ['1', '2', '3', '4'],
        ['1', '2', '3', '4', '5']
    ]

    result = tsp.fit(input_data)

    expected = [
        ['1', '2', '3', '0', '0'],
        ['1', '2', '3', '4', '0'],
        ['1', '2', '3', '4', '5']
    ]

    assert result == expected
