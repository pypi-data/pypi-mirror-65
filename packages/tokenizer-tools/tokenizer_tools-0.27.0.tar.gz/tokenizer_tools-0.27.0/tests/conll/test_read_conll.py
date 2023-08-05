from tokenizer_tools.conll.reader import read_conll


def test_read_conll(datadir):
    result = read_conll(datadir / "data.conll")

    expected = [[["1  a"], ["2  b"]], [["11 a1"], ["21 b1"], [""]]]

    assert result == expected
