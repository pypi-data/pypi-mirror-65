from tokenizer_tools.conll.tag_collector import tag_collector, collect_tag_to_file
from tokenizer_tools.conll.writer import write_conll
def test_tag_collector():
    s = tag_collector(['2.txt'])
    expect = {"a", "b", "a1", "b1"}
    assert s == expect

def test_collect_tag_to_file():
    s = collect_tag_to_file(['3.txt'], '4.txt')

def test_write_conll():
    data = {
      '1': ['a'], 'b':['dff'], 'c': ['1', '3'], 'd':[]
    }
    write_conll(data, '6.txt')

