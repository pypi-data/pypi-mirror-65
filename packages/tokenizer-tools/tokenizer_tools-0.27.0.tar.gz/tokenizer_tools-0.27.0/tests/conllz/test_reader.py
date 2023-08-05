from tokenizer_tools.conllz.reader import read_conllx_from_string, read_conllz_from_string,\
read_conllz,read_conllx

def test_read_conllx_from_string():
    # TODO this way to test has no affect?
    for i in read_conllz_from_string('today is a happy day'):
        print('read_conllz_from_string:',i)

def test_read_conllz_from_string():
    for i in read_conllz_from_string(" the weather is nice"):
        print('read_conllz_from_string:', i)

def test_read_conllz():
    s = read_conllz(open('corpus1.txt'))
    print(s)


def test_read_conllx():
    s = read_conllx(open('corpus1.txt'))
    print(s)
