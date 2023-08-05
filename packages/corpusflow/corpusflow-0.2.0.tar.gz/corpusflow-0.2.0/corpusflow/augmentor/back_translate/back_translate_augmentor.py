import itertools
from typing import List, Any
from corpusflow.augmentor.back_translate.apis import (
    # GoogleCloudTranslate,
    BaiduCloudTranslate,
    # MicrosoftCloudTranslate,
)

# google_translator = GoogleCloudTranslate()
baidu_translator = BaiduCloudTranslate()
# microsoft_translator = MicrosoftCloudTranslate()


def simple_augmenter(
    corpus: List[str],
    max_turn_num: int = 5,
    translator_list: List[Any] = (
        # google_translator,
        baidu_translator,
        # microsoft_translator,
    ),
) -> List[List[str]]:
    # initialize
    previous_doc_list = [[] for _ in corpus]
    augmented_doc_list = [[i] for i in corpus]

    for _ in range(max_turn_num):
        # the change part between current and previous doc list
        delta_doc_list = list(
            map(
                lambda x: list(set(x[0]) - set(x[1])),
                zip(augmented_doc_list, previous_doc_list),
            )
        )

        # update previous doc list
        previous_doc_list = augmented_doc_list

        if not any(len(i) for i in delta_doc_list):
            # the change part is empty, stop iterating
            break

        augmented_delta_doc_list = [[] for _ in corpus]

        for translator in translator_list:
            instance_augmented_doc_list = translator.get_single_turn_augmented_corpus(
                delta_doc_list
            )

            augmented_delta_doc_list = list(
                map(
                    lambda x: list(set(itertools.chain(*x))),
                    zip(augmented_delta_doc_list, instance_augmented_doc_list),
                )
            )

        # merge and remove duplicate then update
        augmented_doc_list = list(
            map(
                lambda x: list(set(itertools.chain(*x))),
                zip(augmented_doc_list, augmented_delta_doc_list),
            )
        )

    return augmented_doc_list


if __name__ == "__main__":
    corpus = ["能在这里报名德语培训吗？", "学生有经常开口说德语的机会吗？"]
    augmented_corpus = simple_augmenter(corpus)
    print(augmented_corpus)
