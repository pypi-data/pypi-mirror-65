from unittest import mock

import numpy as np

from deliverable_model.request import Request
from deliverable_model.response import Response
from deliverable_model.serving.deliverable_model import DeliverableModel
from deliverable_model.serving.model.model import Model
from deliverable_model.serving.processor.processor import Processor


def test_serving(datadir):
    class FakedProcessor:
        def preprocess(self, request):
            # Do nothing
            return request

        def postprocess(self, response):
            # Do nothing
            return response

    class FakedModel:
        def inference(self, request):
            return Response([["tag-{}".format(i) for i in j] for j in request.query])

    mock_load_processor = mock.patch.object(
        Processor, "_instance_single_processor", return_value=FakedProcessor()
    )

    mock_load_model = mock.patch.object(Model, "load", return_value=FakedModel())

    with mock_load_processor, mock_load_model:
        deliverable_model = DeliverableModel.load(datadir)

        request = Request(["abc", "cba"])

        response = deliverable_model.inference(request)

        assert np.all(
            response.data == [["tag-a", "tag-b", "tag-c"], ["tag-c", "tag-b", "tag-a"]]
        )
