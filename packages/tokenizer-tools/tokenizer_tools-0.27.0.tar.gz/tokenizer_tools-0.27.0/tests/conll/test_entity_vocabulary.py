
from tokenizer_tools.conll.entity_vocabulary import entity_vocabulary

def test_entity_vocabulary():
    f = entity_vocabulary(['1.txt'])
    expect = {'a': ['1'], 'b': ['2'], 'a1': ['11'], 'b1': ['21']}
    assert f == expect

