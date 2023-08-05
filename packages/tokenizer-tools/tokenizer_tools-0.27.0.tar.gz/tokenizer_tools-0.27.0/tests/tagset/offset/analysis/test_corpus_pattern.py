from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.analysis.corpus_pattern import CorpusPattern


def test_create_from_corpus(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")

    result = CorpusPattern.create_from_corpus(corpus)

    result_str_list = sorted([str(i) for i in result])

    expected_str_list = sorted(["<PERSON> 在 <GPE> 的 <ORG> 读 书 。", "来 一 首 <歌手名> 的 歌 。"])

    for r, e in zip(result_str_list, expected_str_list):
        assert e in r


def test_render(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")

    corpus_pattern = CorpusPattern.create_from_corpus(corpus)

    dictionary = {
        "PERSON": ["小王", "小李"],
        "GPE": ["北京"],
        "ORG": ["师范大学","专科学校"],
        "歌手名": ["周杰伦", "孙燕姿"]
    }

    generated_corpus = corpus_pattern.render(dictionary)

    expected = sorted([
        "[小 王](PERSON) 在 [北 京](GPE) 的 [师 范 大 学](ORG) 读 书 。",
        "[小 王](PERSON) 在 [北 京](GPE) 的 [专 科 学 校](ORG) 读 书 。",
        "[小 李](PERSON) 在 [北 京](GPE) 的 [师 范 大 学](ORG) 读 书 。",
        "[小 李](PERSON) 在 [北 京](GPE) 的 [专 科 学 校](ORG) 读 书 。",
        "来 一 首 [周 杰 伦](歌手名) 的 歌 。",
        "来 一 首 [孙 燕 姿](歌手名) 的 歌 。"
    ])

    result = sorted([str(i) for i in generated_corpus])

    for e, r in zip(expected, result):
        assert e in r

def test_write_to_file(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")

    corpus_pattern = CorpusPattern.create_from_corpus(corpus)

    corpus_pattern.write_to_file("temp.md")

def test_read_from_file(datadir):
    corpus_pattern = CorpusPattern.read_from_file(datadir / "pattern.md")

    corpus_pattern
    corpus_pattern.write_to_file("temp2.md")
