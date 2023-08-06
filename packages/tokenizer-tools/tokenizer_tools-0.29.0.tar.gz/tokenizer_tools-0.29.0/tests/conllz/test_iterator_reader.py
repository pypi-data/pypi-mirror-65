from tokenizer_tools.conllz.iterator_reader import (
    read_conllx_iterator,
    read_conllx_from_string,
    iterator_reader,
    conllx_iterator_reader,
    read_conllz_iterator,
)

# iterator single file
def test_read_conllz_iterator(datadir):
    for i in read_conllz_iterator(datadir / "corpus.txt"):
        print(i)


# iterator file list
def test_iterator_reader(datadir):
    for i in iterator_reader([datadir / "corpus.txt"]):
        print(i)


def test_read_conllx_iterator(datadir):
    for i in read_conllx_iterator(datadir / "corpus1.txt"):
        print(i)


def test_conllx_iterator_reader(datadir):
    for i in conllx_iterator_reader([datadir / "corpus1.txt"]):
        print(i)
