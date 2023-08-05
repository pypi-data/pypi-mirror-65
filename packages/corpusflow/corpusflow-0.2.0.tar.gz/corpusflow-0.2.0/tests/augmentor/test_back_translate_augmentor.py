from typing import List

from corpusflow.augmentor.back_translate.back_translate_augmentor import (
    simple_augmenter,
)


def test_back_translate_augmentor():
    class FakedTranslatorOne:
        def get_single_turn_augmented_corpus(
            self, corpus: List[List[str]]
        ) -> List[List[str]]:
            return [[str((int(i) + 1) % 10) for i in j] for j in corpus]

    faked_translate_one = FakedTranslatorOne()

    class FakedTranslatorTwo:
        def get_single_turn_augmented_corpus(
            self, corpus: List[List[str]]
        ) -> List[List[str]]:
            return [[str(10 - (int(i) % 10)) for i in j] for j in corpus]

    faked_translate_two = FakedTranslatorTwo()

    corpus = ["1", "2"]

    # test case: one turn
    result = simple_augmenter(
        corpus,
        max_turn_num=1,
        translator_list=[faked_translate_one, faked_translate_two],
    )

    expected = [["1", "2", "9"], ["2", "8", "3"]]

    assert [set(i) for i in result] == [set(i) for i in expected]

    # test case: two turn
    result = simple_augmenter(
        corpus,
        max_turn_num=2,
        translator_list=[faked_translate_one, faked_translate_two],
    )

    expected = [["2", "9", "3", "0", "8", "1"], ["8", "3", "9", "4", "2", "7"]]

    assert [set(i) for i in result] == [set(i) for i in expected]

    # test case: three turn
    result = simple_augmenter(
        corpus,
        max_turn_num=3,
        translator_list=[faked_translate_one, faked_translate_two],
    )

    expected = [
        ["2", "9", "3", "0", "8", "1", "4", "7", "9", "10"],
        ["8", "3", "9", "4", "2", "7", "0", "5", "1", "6"],
    ]

    assert [set(i) for i in result] == [set(i) for i in expected]
