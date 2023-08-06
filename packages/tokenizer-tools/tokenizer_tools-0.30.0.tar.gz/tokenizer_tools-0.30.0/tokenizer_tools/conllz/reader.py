import json

from tokenizer_tools.conllz.sentence import SentenceX


def read_conllx_from_string(conllx_string):
    raw_sentence_list = conllx_string.split("\n\n")

    for raw_sentence in raw_sentence_list:
        cleaned_sentence = raw_sentence.strip()

        if not cleaned_sentence:
            # skip
            continue

        sentence = SentenceX()
        raw_line_list = raw_sentence.split("\n")
        for index, raw_line in enumerate(raw_line_list):
            if index == 0:
                meta_string = raw_line.strip("#\t\n ")
                meta_data = json.loads(meta_string)
                sentence.id = meta_data.pop("id")
                sentence.meta = meta_data

                continue  # read id is done

            # line = raw_line.strip()
            item = raw_line.split("\t")

            if not raw_line or not item:
                # skip
                continue

            sentence.write_as_row(item)

        yield sentence


def read_conllx(input_fd):
    sentence_list = []

    content = input_fd.read()

    for sentence in read_conllx_from_string(content):
        sentence_list.append(sentence)

    return sentence_list
