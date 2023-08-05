from corpusflow.io import read_markdown
from corpusflow.core import Document, DocumentPattern


def test_read_markdown(datadir):
    data_file = datadir / "data.md"

    with data_file.open() as fd:
        raw_result = read_markdown(fd)

    # check if str match
    expected_str_snippet = [
        "this is [#1](order) corpus. xxx. yyy.",
        "this is <entity> corpus",
        "this is #3 corpus. xxx. yyy.",
        "this is #4 corpus"
    ]

    result_str = [str(i) for i in raw_result]

    for i, result_doc_str in enumerate(result_str):
        expected_doc_str = expected_str_snippet[i]
        assert expected_doc_str in result_doc_str

    # check if type match
    expected_type = [
        Document,
        DocumentPattern,
        Document,
        Document
    ]

    for i, result_doc_obj in enumerate(raw_result):
        expected_doc_type = expected_type[i]
        assert isinstance(result_doc_obj, expected_doc_type)
