import concurrent.futures
import os
import uuid
from collections import Counter
from typing import List, Tuple

import requests
from micro_toolkit.data_process.batch_iterator import BatchingIterator

from corpusflow.augmentor.back_translate.apis.microsoft_lang_code import lang_list

# key_var_name = "TRANSLATOR_TEXT_SUBSCRIPTION_KEY"
# if not key_var_name in os.environ:
#     raise Exception(
#         "Please set/export the environment variable: {}".format(key_var_name)
#     )
# subscription_key = os.environ[key_var_name]
subscription_key = "7257875ed5784ad7a4a283b759158b49"

# TODO: the endpoint given by Azure is not working
# endpoint_var_name = "TRANSLATOR_TEXT_ENDPOINT"
# if not endpoint_var_name in os.environ:
#     raise Exception(
#         "Please set/export the environment variable: {}".format(endpoint_var_name)
#     )
# endpoint = os.environ[endpoint_var_name]
# BUT: this one does
# endpoint = "https://api.cognitive.microsofttranslator.com"
endpoint = "https://api-apc.cognitive.microsofttranslator.com"


class MicrosoftCloudTranslate:
    # https://docs.microsoft.com/en-us/azure/cognitive-services/translator/request-limits

    def __init__(self):
        pass

    def get_lang_list(self, except_zh=False):
        if except_zh:
            return list(filter(lambda x: x != self.get_zh_lang(), lang_list))
        return lang_list

    def get_zh_lang(self):
        return "zh-Hans"

    def back_translate_corpus(self, text: List[str]) -> dict:
        return self._back_translate_corpus_with_multi_thread(text)

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

    def _back_translate_corpus_with_multi_thread(self, text: List[str]) -> dict:
        back_translation_dict = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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

    def translate_corpus(self, text: List[str], target_language="en") -> List[str]:
        translate_result = self._translate(text, target_language)
        return translate_result

    def translate(self, text: str, target_language="en") -> str:
        translate_result = self._translate([text], target_language)
        return translate_result[0]

    def _translate(self, text: List[str], target_language="en") -> List[dict]:
        full_result = []

        batch_iterator = BatchingIterator(10)
        for batched_text in batch_iterator(text):
            path = "/translate?api-version=3.0"
            params = "&to={}".format(target_language)
            constructed_url = endpoint + path + params

            headers = {
                "Ocp-Apim-Subscription-Key": subscription_key,
                "Content-type": "application/json",
                "X-ClientTraceId": str(uuid.uuid4()),
            }

            body = [{"text": i} for i in batched_text]

            request = requests.post(constructed_url, headers=headers, json=body)
            response = request.json()

            # for i in response:
            #     if "error" in i.keys():
            #         raise ValueError(response)

            try:
                result = [i["translations"][0]["text"] for i in response]
            except TypeError:
                print(response)
                raise

            full_result.extend(result)

        return full_result

    def get_augmented_text(self, text):
        lang_list_count = len(self.get_lang_list(except_zh=True))

        min_vote_count = max(4, 0.1 * lang_list_count)
        candidate_list = []

        result = self.back_translate(text)
        print(result)

        counter = Counter(result.values())
        print(counter)
        for candidate, count in counter.most_common():
            if count > min_vote_count:
                candidate_list.append((candidate, count / lang_list_count))
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
    g = MicrosoftCloudTranslate()
    result = g.get_augmented_text("能在这里报名德语培训吗？")
    print(result)
