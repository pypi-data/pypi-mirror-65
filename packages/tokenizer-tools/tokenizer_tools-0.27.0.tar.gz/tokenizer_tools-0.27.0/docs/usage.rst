=====
Usage
=====

To use Tokenizer Tools in a project:

.. code-block:: bash

    import tokenizer_tools

**************
常见操作
**************

语料集读写
============
语料集只要通过 Corpus 对象来操作，下面介绍语料集的读和写。

语料集读取
------------
任务：

    读取 corpus.collx 文件，遍历打印每一条语料。

代码：

.. code-block:: python

    from tokenizer_tools.tagset.offset.corpus import Corpus

    corpus = Corpus.read_from_file("corpus.conllx")
    for document in corpus:
        print(document)  # document 就是单条语料对象, 其类型是 Document, 详情见下文

语料集写入
-----------
任务：

    将多条语料写入 corpus.conllx 文件

代码：

.. code-block:: python

    from tokenizer_tools.tagset.offset.corpus import Corpus

    # corpus_item_one 和 corpus_item_two 都是 Document 对象，如何从零构建 Document 对象见下文
    corpus_list = [corpus_item_one, corpus_item_two]

    corpus = Corpus(corpus_list)
    corpus.write_to_file("corpus.conllx")

属性
----------

\__len__
^^^^^^^^^^^^^^^^

通过 len(corpus) 的可以获得语料集中语料（Document 对象）的数量。

\__iter__
^^^^^^^^^^^^^^

通过 for i in corpus 的方式，可以逐一访问语料集中的每一个语料（也就是 i, 类型是 Document).

方法
--------

train_test_split
^^^^^^^^^^^^^^^^^^^^^^^^
划分语料为训练集和测试集，具体参数请参考（sklearn.model_selection.train_test_split）

\__getitem__
^^^^^^^^^^^^^^^^^^^
Corpus 对象支持 corpus[index] 操作，index 对象可以是标量（也就是一个int型数字），也可以是 numpy 数组或者 list 数组（元素类型为 int).
前者返回单个语料（Document 对象），后者返回一个由指定语料组成的语料集（Corpus) 对象。

remove_duplicate
^^^^^^^^^^^^^^^^^^^^^^^^^^^
返回一个去除重复语料（相同的语料具有相同的 text、domian、function、sub_function 和 intent）后的语料集对象。

Document 属性和方法
=======================

每一个单条语料都是一个 Document 对象，现在介绍这个对象所拥有的属性和方法

实例化
-----------
构建一个 Document 对象是十分容易的

.. code-block:: python

    from tokenizer_tools.tagset.offset.corpus import Document
    from tokenizer_tools.tagset.offset.span import Span
    from tokenizer_tools.tagset.offset.span_set import SpanSet

    text = "我要听周杰伦的七里香。"

    document = Document(text)
    document.domain = "导航"  # 设置领域
    document.function = "导航至街道"  # 设置功能点
    document.sub_function = "无"  # 设置子功能点
    document.intent = "导航"  # 设置意图

    # 构建实体集合
    span_list = [
        Span(start=3, end=6, entity="歌手"),
        Span(start=7, end=10, entity="歌曲"),
    ]

    document.entities = SpanSet(span_list)

    # 构建完毕


属性
-----------

text
^^^^^^^^^^^
类型是 list， 代表文本的字段

domain
^^^^^^^^^^^
类型是 string， 代表领域

function
^^^^^^^^^^^^
类型是 string， 代表功能点

sub_function
^^^^^^^^^^^^^^^^^^
类型是 string，代表子功能点

intent
^^^^^^^^^^^^
类型是 string， 代表意图

entities
^^^^^^^^^^^^^^
类型是 SpanSet， 代表实体，下文有详细介绍

方法
------------

compare_entities
^^^^^^^^^^^^^^^^^^^^^^^^^^^
比较文本和实体是否匹配

convert_to_md
^^^^^^^^^^^^^^^^^^^^^
将文本和实体转换成 markdown 格式，用于文本化渲染输出


SpanSet 属性和方法
====================

方法
------

\__iter__
^^^^^^^^^^^^^^^
可以像列表一样访问，得到的每一个元素都是 Span 对象

.. code-block:: python

    for span in span_set:  # span_set 是一个 SpanSet 对象
        print(span)

check_overlap
^^^^^^^^^^^^^^^^^^^^^^
检查 span 是否重叠; 返回 False  表示测试通过，也就是没有重叠, True 表示重叠.

fill_text(text)
^^^^^^^^^^^^^^^^^

按照 text 里面的值，根据每一个 span 对象的 start end 字段提取后并赋值给相应的 value

Span 属性和方法
=============================

属性
-------

start
^^^^^^^^^^^
int, 从 0 开始，包含该位置的字符, 和 Python 中 list[start: end] 类似

end
^^^^^^^^
int， 从0开始，不包含该位置字符, 和 Python 中 list[start: end] 类似

entity
^^^^^^^^^^^^
string， 实体类型

value
^^^^^^^^^^^^^
string， 实体的值, 为了节约内存，通常情况下，该变量的值为 None, 通过调用 span 或者 SpanSet 的 fill_text 方法。

方法
---------

fill_text(text)
^^^^^^^^^^^^^^^^^

按照 text 里面的值，根据 start end 字段提取后并赋值给 value
