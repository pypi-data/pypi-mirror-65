from tokenizer_tools.conllz.tag_collector import (
    tag_collector,
    collect_tag_to_file,
    entity_collector,
    collect_entity_to_file,
    label_collector,
    extra_attr_collector,
    collect_extra_attr_to_file,
    collect_label_to_file,
)


def test_tag_collector(datadir):
    s = tag_collector([datadir / "corpus.txt"])
    print(s)


def test_collect_tag_to_file(datadir):
    collect_tag_to_file([datadir / "corpus3.txt"], datadir / "corpus4.txt")


def test_entity_collector(datadir):
    s = entity_collector([datadir / "corpus3.txt"])
    print(s)


def test_collect_entity_to_file(datadir):
    entity_collector([datadir / "corpus3.txt"])


def test_label_collector(datadir):
    s = label_collector([datadir / "corpus3.txt"])


def test_extra_attr_collector(datadir):
    extra_attr_collector([datadir / "corpus3.txt"])


def test_collect_extra_attr_to_file(datadir):
    collect_extra_attr_to_file([datadir / "corpus3.txt"], datadir / "corpus4.txt")


def test_collect_label_to_file(datadir):
    collect_label_to_file([datadir / "corpus3.txt"], datadir / "corpus4.txt")
