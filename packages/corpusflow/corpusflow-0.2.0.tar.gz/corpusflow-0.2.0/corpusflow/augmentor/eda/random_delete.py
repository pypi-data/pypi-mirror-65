import math
import random
from typing import List


class RandomDelete:
    def __init__(self, alpha: float, prob: float, max_num_per_doc: int):
        self.alpha = alpha
        self.prob = prob
        self.max_num_per_doc = max_num_per_doc

    def __call__(self, corpus: List[List[str]]) -> List[List[str]]:
        result_doc_list = []
        for doc in corpus:
            for _ in range(self.max_num_per_doc):
                new_doc = self._delete_doc(doc)
                result_doc_list.append(new_doc)

        result_corpus = list(result_doc_list)
        return result_corpus

    def _delete_doc(self, doc):
        # TODO: idx selection should return a function, no truly random
        new_doc = doc.copy()
        if len(new_doc) <= 1:
            return new_doc
        if random.uniform(0, 1) > self.prob:
            return new_doc

        replace_times = max(1, int(math.ceil(self.alpha * len(doc))))
        num_replaced = 0
        while len(new_doc):
            if num_replaced >= replace_times:
                break

            random_idx = random.randint(0, len(new_doc) - 1)
            del new_doc[random_idx]
            num_replaced += 1

        return new_doc


if __name__ == "__main__":
    sr = RandomDelete(0.1, 0.8, 10)
    result = sr([["王小明", "在", "北京", "的", "清华大学", "读书", "。"]])
    assert len(result) == 10
