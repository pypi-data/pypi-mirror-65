from tokenizer_tools.converter.conllz_to_offset import conllz_to_offset, conllx_to_offset
from tokenizer_tools.conllz.sentence import Sentence,SentenceX

#TODO
def test_conllz_to_offset():
    sequence = ['B-I', 'B-L']
    rs = conllz_to_offset(sequence)
    print(rs)

#TODO
def test_conllx_to_offset():
    sentence = SentenceX()
    sentence.attribute_lines['0', '3', '8']
    sentence.attribute_names['B-I', 'B-L', 'B-0']
    rs = conllx_to_offset(sentence)
    print(rs)

