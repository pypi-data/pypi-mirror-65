import pytest

from corpusflow.augmentor.back_translate.apis.microsoft_cloud_translate import (
    MicrosoftCloudTranslate,
)


@pytest.mark.skip("faked translation API required")
def test_translate_corpus():
    t = MicrosoftCloudTranslate()
    corpus = ["能在这里报名德语培训吗？", "学生有经常开口说德语的机会吗？"]
    result = t.translate_corpus(corpus)

    assert isinstance(result, list)
    expected_len = 2
    assert len(result) == expected_len


@pytest.mark.skip("faked translation API required")
def test_back_translate_corpus():
    t = MicrosoftCloudTranslate()
    corpus = ["能在这里报名德语培训吗？", "学生有经常开口说德语的机会吗？"]
    result = t.back_translate_corpus(corpus)

    assert isinstance(result, dict)


@pytest.mark.skip("faked translation API required")
def test_get_augmented_corpus():
    t = MicrosoftCloudTranslate()
    corpus = ["能在这里报名德语培训吗？", "学生有经常开口说德语的机会吗？"]
    result = t.get_augmented_corpus(corpus)

    assert isinstance(result, list)
    expected_len = 2
    assert len(result) == expected_len
