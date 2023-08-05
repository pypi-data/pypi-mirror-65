from typing import List, Dict, Tuple


class BaseTranslate:
    def __init__(self, lang_list):
        self.lang_list = lang_list

    def get_lang_list(self, except_zh=False) -> List[str]:
        """
        get a list of language code that current translator supported
        """
        raise NotImplementedError

    def get_zh_lang(self) -> str:
        """
        get the Chinese language code
        """
        raise NotImplementedError

    def translate(self, text: str, target_language="en") -> str:
        """
        translate a single Chinese string into target language
        """
        raise NotImplementedError

    def translate_corpus(self, text: List[str], target_language="en") -> List[str]:
        """
        translate a list of Chinese string into list of target language
        """
        raise NotImplementedError

    def get_augmented_text(self, text: str) -> List[str]:
        """
        translate a single Chinese string into list of augmented Chinese string by back translation
        """
        raise NotImplementedError

    def get_augmented_corpus(self, text: List[str]) -> List[List[str]]:
        """
        translate a list of Chinese string into list of list augmented Chinese string by back translation
        echo inner list of string is augmented for single input string in the same index
        """
        raise NotImplementedError

    def get_multi_turn_augmented_corpus(self, text: List[str], turn_num: int) -> List[List[str]]:
        raise NotImplementedError

    def get_single_turn_augmented_corpus(self, text: List[List[str]]) -> List[List[str]]:
        """
        translate a list of list Chinese string into a list of list augmented Chinese string by back translation
        each inner list of input is a group of same semantic string (list of string).
        each inner list of output is the merged list of augmented result of each string in the same index in input
        """
        raise NotImplementedError

    def filter_candiate(self, candidates: List[str]) -> List[Tuple[str, float]]:
        """
        filter a list of augmented string back translated from different language to few best string with score.
        filter will use min_vote_count_policy to do the filter's job.
        the score is computed as the count of same string in all the string, divided by candidates number.
        """
        raise NotImplementedError

    def min_vote_count_policy(self) -> int:
        """
        compute the threshold (min count) of output result in filter_candidate, which should consider absolute count (at least 2) and the number of back translated language.
        """
        raise NotImplementedError

    def back_translate(self, text: str) -> Dict[str, str]:
        """
        back translate a single Chinese string into a dict
        which the key is intermediate language and the value is back translated single Chinese string
        """
        raise NotImplementedError

    def back_translate_corpus(self, text: List[str]) -> Dict[str, List[str]]:
        """
        back translate a list of Chinese string into a dict
        which the key is intermediate language and the value is the back translated list of Chinese string (same size as the input list)
        """
        raise NotImplementedError

    def _back_translate_corpus_worker(self, text: List[str], target_language: str) -> List[str]:
        """
        back translate a list of Chinese string into a list of back translated Chinese string via intermediate of target_language
        """
        raise NotImplementedError

    def back_translate_with_single_thread(self, text: List[str]) -> Dict[str, List[List[str]]]:
        raise NotImplementedError

    def back_translate_with_multiple_thread(self, text: List[str]) -> Dict[str, List[List[str]]]:
        raise NotImplementedError

    def _back_translate_cropus_multiple_thread_worker(self, text: List[str], target_language) -> List[str]:
        raise NotImplementedError

    def cli(self):
        raise NotImplementedError
