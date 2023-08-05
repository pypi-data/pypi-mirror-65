import math
import random
from typing import List, Callable


class RandomSwap:
    def __init__(self, alpha: float, max_num_per_doc: int):
        self.alpha = alpha
        self.max_num_per_doc = max_num_per_doc

    def __call__(self, corpus: List[List[str]]) -> List[List[str]]:
        result_doc_list = []
        for doc in corpus:
            for _ in range(self.max_num_per_doc):
                new_doc = self._swap_doc(doc)
                result_doc_list.append(new_doc)

        result_corpus = list(result_doc_list)
        return result_corpus

    def _swap_doc(self, doc):
        # TODO: idx_need_swap need replace by a function which is not truly random
        replace_times = max(2, int(math.ceil(self.alpha * len(doc))))
        new_doc = doc.copy()

        while True:
            random_idx = list(range(len(new_doc)))
            random.shuffle(random_idx)
            idx_need_swap = random_idx[:replace_times]
            idx_in_doc = sorted(idx_need_swap)
            if idx_need_swap != idx_in_doc:
                break

        for from_idx, to_idx in zip(idx_in_doc, idx_need_swap):
            new_doc[to_idx] = doc[from_idx]

        return new_doc


if __name__ == "__main__":

    def faked_synoym_func(input):
        data = {"北京": ["上海", "杭州"], "读书": ["上学"], "清华大学": ["北京大学"]}
        return data.get(input, [])

    sr = RandomSwap(0.1, 4)
    result = sr([["王小明", "在", "北京", "的", "清华大学", "读书", "。"]])
    assert len(result) == 4
