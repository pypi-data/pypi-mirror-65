=====
Usage
=====

To use corpusflow in a project::

    import corpusflow

**************
常见操作
**************

语料集读写
============

语料集是通过 Corpus 对象来操作的，下面介绍语料集的读和写。

语料集读取
------------
任务：

    读取 corpus.collx 文件，遍历打印每一条语料。

代码：

.. code-block:: python

    from corpusflow import Corpus

    corpus = Corpus.read_from_file("corpus.conllx")
    for document in corpus:
        print(document)  # document 就是单条语料对象, 其类型是 Document, 详情见下文

语料集写入
-------------
任务：

    将多条语料写入 corpus.conllx 文件

代码：

.. code-block:: python

    from corpusflow import Corpus

    # corpus_item_one 和 corpus_item_two 都是 Document 对象，如何从零构建 Document 对象见下文
    corpus_list = [corpus_item_one, corpus_item_two]

    corpus = Corpus(corpus_list)
    corpus.write_to_file("corpus.conllx")

Corpus 属性
-------------

Corpus 具有很多 Python 内建 list 类所拥有的属性和方法，大部分情况下 list 类所拥有的属性和方法，都可以安全的在 Corpus 类上使用。

\__len__
^^^^^^^^^^^^^^^^

通过 len(corpus) 的可以获得语料集中语料（Document 对象）的数量。

代码：

.. code-block:: python

   # corpus 是一个 Corpus 对象
   corpus_size = len(corpus)  # corpus_size 是一个 int 型变量，其值是 corpus 对象中 Document 的数量。

\__iter__
^^^^^^^^^^^^^^

通过 for doc in corpus 的方式，可以逐一访问语料集中的每一个语料（也就是 doc, 类型是 Document).

代码：

.. code-block:: python

   # corpus 是一个 Corpus 对象
   for doc in corpus:
       print(doc)  # doc 变量的类型是 Document

方法
--------

[类方法]read_from_file
^^^^^^^^^^^^^^^^^^^^^^^^^
此方法为类方法，用于从 conllx 文件读入数据并返回一个类型为 Corpus 的对象。传入参数只有一个，就是文件的路径。

write_to_file
^^^^^^^^^^^^^^^^^^^^^
参数为要输出的文件路径，调用该方法后，Corpus 对象所表示的语料数据就会被写入到所指定的文件。

union
^^^^^^^^^^^^
这个操作和 Python 内建类型 set 一样，用于求两个或者多个 Corpus 对象中 Document 的并集。

intersection
^^^^^^^^^^^^^^^^^
这个操作和 Python 内建类型 set 一样，用于求两个或者多个 Corpus 对象中 Document 的交集。

difference
^^^^^^^^^^^^^^^^^
这个操作和 Python 内建类型 set 一样，用于求出现在本 Corpus 对象中但不存在与其他一个或者多个 Corpus 对象中的 Document。

symmetric_difference
^^^^^^^^^^^^^^^^^^^^^^^^^
这个操作和 Python 内建类型 set 一样，多个 Corpus 的 symmetric_defference. The symmetric difference of two sets A and B is the set of elements that are in either A or B , but not in their intersection. 。

remove_duplicate
^^^^^^^^^^^^^^^^^^^^^^
用于移除 corpus 中的“重复”的 Document。

generate_statistics
^^^^^^^^^^^^^^^^^^^^^^^^^
对当前 Corpus 对象生成统计信息，返回一个 CorpusStatistics 对象。包含多种纬度的统计信息。

get_doc_by_id
^^^^^^^^^^^^^^^^^^
按照 document id （每个 document 都有一个 ID， str 类型），获取 document 对象。

get_all_doc_ids
^^^^^^^^^^^^^^^^^^^
获取所有的 doc id，返回的是一个列表

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

实例化一个 Document 对象
--------------------------
构建一个 Document 对象是十分容易的

.. code-block:: python

    from corpusflow import Document
    from corpusflow import Span
    from corpusflow import SpanSet

    text = "我要听周杰伦的七里香。"

    document = Document(text)
    document.domain = "导航"  # 设置领域
    document.function = "导航至街道"  # 设置功能点
    document.sub_function = "无"  # 设置子功能点
    document.intent = "导航"  # 设置意图

    # 构建实体集合
    span_list = [
        Span(start=3, end=6, entity="歌手"),  # start/end 都是从 0 开始计数，设置 从 3（包含 3） 到 6（不包含 6）的字符实体是歌手。
        Span(start=7, end=10, entity="歌曲"),  # start 和 end 和 Python 中的 slice 操作一样，也就是 text[start : end] 的实体是歌手。
    ]

    document.entities = SpanSet(span_list)  # 为 Document 的实体设置 span_set

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

fill_text(text）
^^^^^^^^^^^^^^^^^

按照 text 里面的值，根据 start end 字段提取后并赋值给 value

***********************************************
如何更改在 Corpus 比较中的 Document 比较方法
***********************************************

针对不同的任务和场景，可能需要不同的 Document 比较方案，单一的比较方案难以满足，为此 CorpusFlow 提供了多种内建的比较方案(用户可以自定义比较方案)，并提供了动态改变比较方案的方法。

下面的方案其优先级依次增加：同时使用时，后者会覆盖前者的效果。

全局性改变对比方案
=====================

.. code-block:: python

   corpus_set_compare_way(xxx)


利用上下文管理器改变对比方案
==============================

.. code-block:: python

   with CorpusCompareContext(XXX):
       ...

Corpus 级别的改变
===================

.. code-block:: python

   corpus.set_compare_way(XXX)


******************************************
实体绑定与语料修改
******************************************
为了明确使用者的意图，语料的修改做了如下的约束：语料修改分为非实体部分修改和实体部分修改，不允许同时修改非实体和实体。

修改非序列部分
===================
intent, function, sub_function, domain 等都是与序列无关的，他们的修改非常简单

.. code-block:: python

   doc  # 一个 Document 对象
   doc.domain = "new_domain"  # 修改 domain
   doc.function = "new_function"  # 修改 function
   doc.sub_function = "new_sub_function"  # 修改 sub_function
   doc.intent = "new_intent"  # 修改 intent


修改非实体部分
===================
替换

.. code-block:: python

   doc  # 一个 Document 对象
   start = 1; end = 2  # 要替代部分的起始和终止 index
   value = ["a", "b"]  # 待更新的值
   doc.text[start: end] = value
   # 注意：如果切片 text[start:end] 中间包含实体部分，则会报错

插入

.. code-block:: python

   doc  # 一个 Document 对象
   idx  # 待插入位置 index
   value = ["a", "b"]  # 待更新的值
   doc.text.insert(idx, value)
   # 注意：如果 text[idx] 属于某个实体部分，则会报错

删除

.. code-block:: python

   doc  # 一个 Document 对象
   start = 1; end = 2  # 要删除的起始和终止 index
   del doc.text[start: end]
   # 注意: 如果切片 text[start:end] 中间包含实体部分，则会报错


修改实体集
===================
替换

.. code-block:: python

   span_set  # 一个 SpanSet 对象
   start = 1; end = 2  # 要替代部分的起始和终止 index
   value = [span_a, span_b]  # 待更新的值
   span_set[start: end] = value
   # 注意： 如果更新后 span 中间出现 overlap，则会报错

插入

.. code-block:: python

   span_set  # 一个 SpanSet 对象
   idx  # 待插入位置 index
   value = [span_a, span_b]  # 待更新的值
   span_set.insert(idx, value)
   # 注意:  如果更新后 span 中间出现 overlap，则会报错

删除

.. code-block:: python

   span_set  # 一个 SpanSet 对象
   start = 1; end = 2  # 要删除的起始和终止 index
   del span_set[start: end]


修改实体部分
===================

.. code-block:: python

   span  # 一个 Span 对象
   value = ["a", "b"]  # 待更新的值
   span.value = value  # 更新 entity 的值
   span.type = "new_type"  # 更新 entity 的类型


***********************************
句子的表达模式
***********************************
句子的表达模式就是将具体的实体值替换成实体类型就可以得到句子的表达模式。
例如：``[明天](日期)的天气如何？`` 的表达模式就是 ``<日期>的天气如何？``。
利用句子的表达模式，我们了解用户对意图的表达方式有多少种。

模式Document
==============

在 CorpusFlow 中每一个模式都是一个 DocumentPattern 对象，可以通过 render 方法对这个模版进行渲染从而得到真实的语料文档（Document 对象）。

.. code-block:: Python

   dp  # 一个 DocumentPattern 对象
   dp_md = dp.convert_to_md()
   # dp_md 大概内容是 <name>在[北京](city)的<school>读书。
   doc = dp.render(name="小明", school="清华大学")
   # doc 是一个 Document 对象，内容大概是：[小明](name)在[北京](city)的[清华大学](school)读书。


提取语料的表达方式
====================

可以从语料中提取出整个语料的模式，整个语料的模式是一个 CorpusPattern 对象，类似于 Corpus 对象，你可以迭代访问其中的每一个模式（DocumentPattern）。


.. code-block:: python

   corpus_pattern  # 一个 CorpusPattern 对象

   for pattern in corpus_pattern:
       print(pattern)  # 一个 DocumentPattern 对象

从Corpus生成CorpusPattern
--------------------------------

.. code-block:: python

   corpus  # 一个 Corpus 对象
   corpus_pattern = CorpusPattern.create_from_corpus(corpus)
   corpus_pattern  # 一个 CorpusPattern 对象

从文档读入CorpusPattern
--------------------------------

.. code-block:: python

   corpus  # 一个 Corpus 对象
   md_file  # 一个 markdown 文件路径
   corpus_pattern = CorpusPattern.read_from_file(md_file)
   corpus_pattern  # 一个 CorpusPattern 对象

利用表达模式扩充语料
======================

语料的模式（CorpusPattern 对象）是能够集体渲染的，通过 render 方法，可以对 CorpusPattern 中的每一个模板（DocumentPattern 对象）进行渲染，最终结果是一个 Corpus 对象。

.. code-block:: python

    corpus_pattern  # 一个 CorpusPattern 对象

    dictionary = {
        "PERSON": ["小王", "小李"],
        "GPE": ["北京"],
        "ORG": ["师范大学","专科学校"],
        "歌手名": ["周杰伦", "孙燕姿"]
    }

    generated_corpus = corpus_pattern.render(**dictionary)
    generated_corpus  # 一个 Corpus 对象，从句子表达模式中结合具体的实体产生的

**********************************
模糊搜索语料
**********************************

Corpus 支持对其中的语料进行模糊搜索。

.. code-block:: python

    corpus  # 一个 Corpus 对象

    search_result = corpus.fuzzy_search("明天 上海")
    search_result  # 一个 list 对象，里面的元素是一个 tuple，第一个子元素是 Document，第二个子元素是得分
