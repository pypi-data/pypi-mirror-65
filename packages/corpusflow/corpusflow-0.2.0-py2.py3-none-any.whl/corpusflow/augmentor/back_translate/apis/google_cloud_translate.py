import copy
import itertools
import os
from collections import Counter
from typing import List, Tuple
import concurrent.futures

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = os.path.expanduser("~/.config/gcloud/Online Computing-2c16cb802e50.json")

from google.cloud import translate_v2 as translate
from corpusflow.augmentor.back_translate.apis.google_lang_code import lang_list
import six


class GoogleCloudTranslate:
    # Quota issue, see https://cloud.google.com/translate/quotas

    def __init__(self):
        self.translate_client = translate.Client()

    def get_lang_list(self, except_zh=False):
        if except_zh:
            return list(filter(lambda x: x != self.get_zh_lang(), lang_list))
        return lang_list

    def get_zh_lang(self):
        return "zh-CN"

    def translate(self, text: str, target_language="en") -> str:
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        result = self.translate_client.translate(text, target_language=target_language)

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        return result["translatedText"]

    def translate_corpus(self, text: List[str], target_language="en") -> List[str]:
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        result = self.translate_client.translate(text, target_language=target_language)

        # print(u"Text: {}".format(result["input"]))
        # print(u"Translation: {}".format(result["translatedText"]))
        # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        return [i["translatedText"] for i in result]

    def get_augmented_text(self, text):
        lang_list_count = len(self.get_lang_list(except_zh=True))

        min_vote_count = max(4, 0.1 * lang_list_count)
        candidate_list = []

        result = self.back_translate(text)

        counter = Counter(result.values())
        for candidate, count in counter.most_common():
            if count > min_vote_count:
                candidate_list.append((candidate, count / lang_list_count))
            else:
                break

        return candidate_list

    def get_multi_turn_augmented_corpus(
        self, text: List[str], turn_num: int
    ) -> List[List[str]]:
        init_corpus: List[List[str]] = [[i] for i in text]
        augmented_corpus: List[List[str]] = None

        for _ in range(turn_num):
            corpus_instance = augmented_corpus if augmented_corpus else init_corpus
            augmented_corpus = self.get_single_turn_augmented_corpus(corpus_instance)

            # remove duplicate
            augmented_corpus = list(map(lambda x: list(set(x)), augmented_corpus))

        return augmented_corpus

    def get_single_turn_augmented_corpus(
        self, text: List[List[str]]
    ) -> List[List[str]]:
        flatten_key_to_nest_key = {}
        flatten_list: List[str] = []
        for nest_key, list_of_str in enumerate(text):
            for str_ in list_of_str:
                flatten_key = len(flatten_list)
                flatten_key_to_nest_key[flatten_key] = nest_key
                flatten_list.append(str_)

        augmented_corpus = self.get_augmented_corpus(flatten_list)
        result_text = [[] for _ in text]
        for flatten_key, list_of_str in enumerate(augmented_corpus):
            nest_key = flatten_key_to_nest_key[flatten_key]
            result_text[nest_key].extend(list_of_str)

        return result_text

    def get_augmented_corpus(self, text: List[str]) -> List[List[str]]:
        back_translate_result = self.back_translate_corpus(text)

        candidates = zip(*back_translate_result.values())

        augmented_corpus_with_score = map(self.filter_candidate, candidates)

        augmented_corpus = list(
            map(lambda x: [i[0] for i in x], augmented_corpus_with_score)
        )

        return augmented_corpus

    def filter_candidate(self, candidates: List[str]) -> List[Tuple[str, float]]:
        # TODO: pre compute those constant should be faster
        lang_list_count = len(self.get_lang_list(except_zh=True))
        min_vote_count = max(4, 0.1 * lang_list_count)

        candidate_list = []

        counter = Counter(candidates)
        for candidate, count in counter.most_common():
            if count > min_vote_count:
                score = count / lang_list_count
                candidate_list.append((candidate, score))
            else:
                break

        return candidate_list

    def back_translate(self, text: str) -> dict:
        back_translation_dict = {}
        for target_lang in self.get_lang_list(except_zh=True):
            translated_text = self.translate(text, target_language=target_lang)
            back_translated_text = self.translate(
                translated_text, target_language=self.get_zh_lang()
            )
            back_translation_dict[target_lang] = back_translated_text

        return back_translation_dict

    def back_translate_corpus(self, text: List[str]) -> dict:
        return self._back_translate_corpus_with_multi_thread(text)

    def _back_translate_corpus_with_single_thread(self, text: List[str]) -> dict:
        back_translation_dict = {}
        for target_lang in self.get_lang_list(except_zh=True):
            translated_text = self.translate_corpus(text, target_language=target_lang)
            back_translated_text = self.translate_corpus(
                translated_text, target_language=self.get_zh_lang()
            )
            back_translation_dict[target_lang] = back_translated_text

        return back_translation_dict

    def _back_translate_corpus_with_multi_thread(self, text: List[str]) -> dict:
        back_translation_dict = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_lang = {
                executor.submit(
                    self._back_translate_corpus, text, target_lang
                ): target_lang
                for target_lang in self.get_lang_list(except_zh=True)
            }
            for future in concurrent.futures.as_completed(future_to_lang):
                target_lang = future_to_lang[future]
                back_translation_dict[target_lang] = future.result()

        return back_translation_dict

    def _back_translate_corpus(
        self, text: List[str], target_lang: str
    ) -> List[str]:
        translated_text = self.translate_corpus(text, target_language=target_lang)
        back_translated_text = self.translate_corpus(
            translated_text, target_language=self.get_zh_lang()
        )

        return back_translated_text

    def cli(self):
        while True:
            word = input("请输入您要翻译的单词:")
            if word >= u"\u4e00" and word <= u"\u9fa6":
                # includes some Chinese char
                target_language = "en"
            else:
                target_language = "zh-CN"
            result = self.translate(word, target_language)
            print("译文:" + result)


if __name__ == "__main__":
    g = GoogleCloudTranslate()
    result = g.get_augmented_text("能在这里报名德语培训吗？")
    print(result)
