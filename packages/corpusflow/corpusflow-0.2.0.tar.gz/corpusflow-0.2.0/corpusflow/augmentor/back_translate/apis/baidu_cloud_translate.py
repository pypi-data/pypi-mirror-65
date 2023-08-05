import concurrent.futures
import hashlib
import http.client
import json
import random
import urllib
from collections import Counter
from typing import List, Tuple, Dict, Any, Union

from micro_toolkit.concurrent.rate_limited_group import RateLimitedGroup
from micro_toolkit.data_process.batch_iterator import BatchingIterator
from tenacity import retry, stop_after_attempt, wait_fixed

from corpusflow.augmentor.back_translate.apis.baidu_lang_code import lang_list


# TODO: refactor below code, let the appid and key load from environment
appid = "20191227000370447"  # 填写你的appid
secretKey = "GG9aQKGDK9SVu9siETWQ"  # 填写你的密钥

httpClient = None
myurl = "/api/trans/vip/translate"


class BaiduCloudTranslate:
    # docs at https://fanyi-api.baidu.com/api/trans/product/apidoc

    def __init__(self, api_rate_limited: float = 80):
        # default rate limited is 80, because consider the full capacity is 100 of 尊像版, 80% of full capacity.

        self.api_rate_limited = api_rate_limited
        self.rate_limited_group = RateLimitedGroup(self.api_rate_limited)

    def get_lang_list(self, except_zh=False):
        if except_zh:
            return list(filter(lambda x: x != self.get_zh_lang(), lang_list))
        return lang_list

    def get_zh_lang(self):
        return "zh"

    def translate(self, text: str, target_language="en") -> str:
        translate_result = self._translate(text, target_language)
        return translate_result[0]["dst"]

    def translate_corpus(self, text: List[str], target_language="en") -> List[str]:
        # since baidu using URL based batch request, It may 414 ('Request-URI Too Long'), so here using batched request
        full_result = []

        batch_iterator = BatchingIterator(10)
        for batched_text in batch_iterator(text):
            text = "\n".join(batched_text)
            translate_result = self._translate(text, target_language)

            full_result.extend([i["dst"] for i in translate_result])

        return full_result

    @retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
    def _translate(self, text: Union[str, List[str]], target_language="en") -> Any:
        with self.rate_limited_group:
            fromLang = "auto"  # 原文语种
            toLang = target_language  # 译文语种
            salt = random.randint(32768, 65536)
            q = text
            sign = appid + q + str(salt) + secretKey
            sign = hashlib.md5(sign.encode()).hexdigest()
            reqeust_url = (
                myurl
                + "?appid="
                + appid
                + "&q="
                + urllib.parse.quote(q)
                + "&from="
                + fromLang
                + "&to="
                + toLang
                + "&salt="
                + str(salt)
                + "&sign="
                + sign
            )

            try:
                httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
                httpClient.request("GET", reqeust_url)

                # response是HTTPResponse对象
                response = httpClient.getresponse()

                assert response.status == 200
                result_all = response.read().decode("utf-8")

                try:
                    result = json.loads(result_all)
                except json.decoder.JSONDecodeError:
                    print("")
                    raise

                # print(result)
                if "trans_result" not in result:
                    raise ValueError("Baidu backend show a different result: {}".format(result))

                return result["trans_result"]

            except Exception as e:
                raise
                # print(e)
            finally:
                if httpClient:
                    httpClient.close()

    def get_augmented_text(self, text):
        lang_list_count = len(self.get_lang_list(except_zh=True))

        min_vote_count = max(4, 0.1 * lang_list_count)
        candidate_list = []

        result = self.back_translate(text)
        # print(result)

        counter = Counter(result.values())
        # print(counter)
        for candidate, count in counter.most_common():
            if count > min_vote_count:
                candidate_list.append((candidate, count / lang_list_count))
            else:
                break

        return candidate_list

    def get_augmented_corpus(self, text: List[str]):
        back_translate_result = self.back_translate_corpus(text)

        candidates = zip(*back_translate_result.values())

        augmented_corpus_with_score = map(self.filter_candidate, candidates)

        augmented_corpus = list(
            map(lambda x: [i[0] for i in x], augmented_corpus_with_score)
        )

        return augmented_corpus

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

    def back_translate_corpus(self, text: List[str]) -> Dict[str, List[str]]:
        return self._back_translate_corpus_with_single_thread(text)

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
                    self._back_translate_corpus_worker, text, target_lang
                ): target_lang
                for target_lang in self.get_lang_list(except_zh=True)
            }
            for future in concurrent.futures.as_completed(future_to_lang):
                target_lang = future_to_lang[future]
                back_translation_dict[target_lang] = future.result()

        return back_translation_dict

    def _back_translate_corpus_worker(
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
    g = BaiduCloudTranslate()
    result = g.get_augmented_text("能在这里报名德语培训吗？")
    print(result)
