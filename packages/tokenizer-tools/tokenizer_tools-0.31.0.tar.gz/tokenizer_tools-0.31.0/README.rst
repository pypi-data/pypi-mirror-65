################
Tokenizer Tools
################


.. image:: https://img.shields.io/pypi/v/tokenizer_tools.svg
        :target: https://pypi.python.org/pypi/tokenizer_tools

.. image:: https://travis-ci.com/howl-anderson/tokenizer_tools.svg?branch=master
        :target: https://travis-ci.com/howl-anderson/tokenizer_tools

.. image:: https://readthedocs.org/projects/tokenizer-tools/badge/?version=latest
        :target: https://tokenizer-tools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/howlandersonn/tokenizer_tools/shield.svg
     :target: https://pyup.io/repos/github/howlandersonn/tokenizer_tools/
     :alt: Updates



Tools/Utils for NLP (including dataset reading, tagset encoding & decoding, metrics computing) | NLP 工具集（包含数据集读取、tagset 编码和解码、指标的计算等）


* Free software: MIT license
* Documentation: https://tokenizer-tools.readthedocs.io.


*********
Features
*********

* 常见数据集格式的读取
* 多种 Tagset 的编码和解码 [`BMES 体系 <tokenizer_tools/tagset/BMES.py>`_, `BILUO 体系 <tokenizer_tools/tagset/NER/BILUO.py>`_, `IOB 体系 <tokenizer_tools/tagset/NER/IOB.py>`_]
* 指标的计算

*******
功能
*******

语料集读写
============

本软件提供了一种语料存储的磁盘文件格式（暂定名为 conllx）和内存对象格式（暂定名为 offset）。

语料集读取
------------
任务：读取 corpus.collx 文件，遍历打印每一条语料。

代码：

.. code-block:: python

    from tokenizer_tools.tagset.offset.corpus import Corpus

    corpus = Corpus.read_from_file("corpus.conllx")
    for document in corpus:
        print(document)  # document 就是单条语料对象

语料集写入
-----------
任务：将多条语料写入 corpus.conllx 文件

代码：

.. code-block:: python

    from tokenizer_tools.tagset.offset.corpus import Corpus

    corpus_list = [corpus_item_one, corpus_item_two]

    corpus = Corpus(corpus_list)
    corpus.write_to_file("corpus.conllx")

Document 属性和方法
=======================

每一个单条语料都是一个 Document 对象，现在介绍这个对象所拥有的属性和方法

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

__iter__
^^^^^^^^^^^^^^^
可以像列表一样访问，得到的每一个元素都是 Span 对象

check_overlap
^^^^^^^^^^^^^^^^^^^^^^
检查 span 是否重叠

Span 属性和方法
=============================

属性
-------

start
^^^^^^^^^^^
int, 从 0 开始，包含该位置

end
^^^^^^^^
int， 从0开始，不包含该位置

entity
^^^^^^^^^^^^
string， 实体类型

value
^^^^^^^^^^^^^
string， 实体的值

******
TODO
******

* 改变项目的名字，tokenizer_tools 已经无法正确描述现在项目的功能

*********
Credits
*********

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
