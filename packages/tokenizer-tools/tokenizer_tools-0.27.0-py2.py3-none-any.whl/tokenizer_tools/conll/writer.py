from tokenizer_tools.utils.deprecated_support import deprecated_support


@deprecated_support()
def write_conll(data, output_file, blank_token='_', conll_format=False):
    with open(output_file, 'wt') as fd:
        for raw_sentence in data:
            sentence = raw_sentence if conll_format else zip(*raw_sentence)
            for raw_row in sentence:
                # convert empty char to `_`
                row = [i if i != " " else blank_token for i in raw_row]
                #TODO why?
                fd.write('{}'.format("\t".join(row)))
                fd.write('\n')

            fd.write('\n')


if __name__ == "__main__":
    pass
