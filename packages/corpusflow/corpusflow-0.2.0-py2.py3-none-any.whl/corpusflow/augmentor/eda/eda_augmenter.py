from typing import List

from corpusflow.augmentor.eda import (
    SynonymReplace,
    RandomDelete,
    RandomInsert,
    RandomSwap,
)


def faked_synonym_func(input):
    data = {
        "北京": ["上海", "杭州", "广州", "深圳"],
        "读书": ["上学", "念书"],
        "清华大学": ["北京大学", "中国人民大学"],
    }
    return data.get(input, [])


# def faked_stopwords_filter(input):
#     stopwords = ["在", "的"]
#     return input not in stopwords

from corpusflow.augmentor.stopwords import stopwords_baidu

black_token_list = ["清华大学"]

replacer = SynonymReplace(faked_synonym_func, stopwords_baidu, black_token_list,
                          0.1, 6)
deleter = RandomDelete(0.1, 0.8, 6)
inserter = RandomInsert(faked_synonym_func, 0.1, 6)
swaper = RandomSwap(0.1, 6)


def simple_augmenter(corpus: List[List[str]]) -> List[List[str]]:
    augmented_doc_list = []

    augmented_doc_list.extend(replacer(corpus))
    augmented_doc_list.extend(deleter(corpus))
    augmented_doc_list.extend(inserter(corpus))
    augmented_doc_list.extend(swaper(corpus))

    return augmented_doc_list


if __name__ == "__main__":
    corpus = [["王小明", "在", "北京", "的", "清华大学", "读书", "。"]]
    augmented_corpus = simple_augmenter(corpus)
    print(augmented_corpus)
