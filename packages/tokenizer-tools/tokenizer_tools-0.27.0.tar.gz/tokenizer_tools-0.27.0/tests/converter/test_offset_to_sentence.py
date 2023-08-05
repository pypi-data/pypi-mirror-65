from tokenizer_tools.converter.offset_to_sentence import offset_to_sentence

#TODO
def test_offset_to_sentence():
    sequence = ['B-O', 'B-I']
    rs = offset_to_sentence()
    print(rs)
