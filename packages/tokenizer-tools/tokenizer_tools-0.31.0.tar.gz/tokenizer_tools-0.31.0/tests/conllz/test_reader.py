from tokenizer_tools.conllz.reader import read_conllx_from_string, read_conllx
import pytest


@pytest.mark.skip("")
def test_read_conllx_from_string():
    # TODO this way to test has no affect?
    for i in read_conllx_from_string("today is a happy day"):
        print("read_conllz_from_string:", i)


@pytest.mark.skip("")
def test_read_conllx_from_string():
    for i in read_conllx_from_string(" the weather is nice"):
        print("read_conllz_from_string:", i)


@pytest.mark.skip("")
def test_read_conllx():
    s = read_conllx(open("corpus1.txt"))
    print(s)
