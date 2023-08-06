from deliverable_model.request import Request
from deliverable_model.response import Response
from deliverable_model.serving.processor.processor import Processor

import numpy as np


def test_serving(datadir):
    metadata = {
        "instance": {
            "LookupProcessor_0": {
                "class": "deliverable_model.builtin.processor.lookup_processor.LookupProcessor",
                "parameter": {
                    "lookup_table": ["vocabulary", "tag"],
                    "padding_parameter": {},
                },
            }
        },
        "pipeline": {"pre": ["LookupProcessor_0"], "post": ["LookupProcessor_0"]},
    }
    processor_obj = Processor.load(datadir, metadata)

    processor_obj.instance_processor()

    request = Request(["abc", "cba"])
    return_request = processor_obj.call_preprocessor(request)

    assert np.all(return_request.query == [[1, 2, 3], [3, 2, 1]])

    response = Response([[1, 2, 3], [3, 2, 1]])
    return_response = processor_obj.call_postprocessor(response)

    assert np.all(
        return_response.data
        == [["tag-a", "tag-b", "tag-c"], ["tag-c", "tag-b", "tag-a"]]
    )
