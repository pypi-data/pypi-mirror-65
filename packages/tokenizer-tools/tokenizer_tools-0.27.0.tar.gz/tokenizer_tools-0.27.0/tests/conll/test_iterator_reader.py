from tokenizer_tools.conll.iterator_reader import iterator_reader


def test_iterator_reader(datadir):
    input_file = list(sorted([i for i in datadir.glob("*") if i.is_file()]))

    output = list(iterator_reader(input_file))

    expected = [
        [["1", "a"], ["2", "b"]],
        [["11", "a1"], ["21", "b1"]],
        [["3", "c"], ["4", "d"]],
        [["31", "c1"], ["41", "d1"]],
    ]
    assert output == expected
