import filecmp

from deliverable_model.builtin.processor.lookup_processor import LookupProcessor
from deliverable_model.request import Request
from deliverable_model.response import Response
from seq2annotation.input import Lookuper
import numpy as np


def test_build(datadir, tmpdir):
    lookup_processor = LookupProcessor()

    vocabulary_lookup_table = Lookuper({"a": 1, "b": 2, "c": 3})
    lookup_processor.add_vocabulary_lookup_table(vocabulary_lookup_table)

    tag_lookup_table = Lookuper({"tag-a": 1, "tag-b": 2, "tag-c": 3})
    lookup_processor.add_tag_lookup_table(tag_lookup_table)

    assert lookup_processor.get_config() == {
        "lookup_table": ["vocabulary", "tag"],
        "padding_parameter": {},
    }

    lookup_processor.serialize(tmpdir)

    match, mismatch, errors = filecmp.cmpfiles(
        datadir, tmpdir, ["tag", "vocabulary"], shallow=False
    )

    assert len(match) == 2


def test_serving(datadir, tmpdir):
    parameter = {"lookup_table": ["vocabulary", "tag"], "padding_parameter": {}}

    lookup_processor = LookupProcessor.load(parameter, datadir)

    request = Request(["abc", "cba"])
    return_request = lookup_processor.preprocess(request)

    assert np.all(return_request.query == [[1, 2, 3], [3, 2, 1]])

    response = Response([[1, 2, 3], [3, 2, 1]])
    return_response = lookup_processor.postprocess(response)

    assert np.all(
        return_response.data
        == [["tag-a", "tag-b", "tag-c"], ["tag-c", "tag-b", "tag-a"]]
    )
