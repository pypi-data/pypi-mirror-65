import math
import random
from typing import Callable, List


class SynonymReplace:
    def __init__(
        self,
        synonym_func: Callable[[str], List[str]],
        stopwords_filter: Callable[[str], bool],
        black_token_list: List[str],
        alpha: float,
        max_num_per_doc: int,
    ):
        self.synonym_func = synonym_func
        self.stopwords_filter = stopwords_filter
        self.black_token_list = black_token_list
        self.alpha = alpha
        self.max_num_per_doc = max_num_per_doc

    def __call__(self, corpus: List[List[str]]) -> List[List[str]]:
        result_doc_list = []
        for doc in corpus:
            for _ in range(self.max_num_per_doc):
                new_doc = self._replace_doc(doc)
                result_doc_list.append(new_doc)

        result_corpus = list(result_doc_list)
        return result_corpus

    def _replace_doc(self, doc):
        replace_times = max(1, int(math.ceil(self.alpha * len(doc))))
        new_doc = doc.copy()
        candidate_token_list = list(filter(self.stopwords_filter, new_doc))
        candidate_token_list = list(
            filter(lambda x: x not in self.black_token_list, candidate_token_list)
        )
        random.shuffle(candidate_token_list)
        num_replaced = 0
        for candidate_token in candidate_token_list:
            if num_replaced >= replace_times:
                break

            token_synonyms = self.synonym_func(candidate_token)
            if len(token_synonyms):
                synonym = random.choice(token_synonyms)
                new_doc = list(
                    map(lambda x: x if x != candidate_token else synonym, new_doc)
                )
                num_replaced += 1

        return new_doc


if __name__ == "__main__":

    def faked_synoym_func(input):
        data = {"北京": ["上海", "杭州"], "读书": ["上学"], "清华大学": ["北京大学"]}
        return data.get(input, [])

    def faked_stopwors_filter(input):
        stopwords = ["在", "的"]
        return input not in stopwords

    black_token_list = ["清华大学"]

    sr = SynonymReplace(
        faked_synoym_func, faked_stopwors_filter, black_token_list, 0.1, 6
    )
    result = sr([["王小明", "在", "北京", "的", "清华大学", "读书", "。"]])
    assert len(result) == 7
