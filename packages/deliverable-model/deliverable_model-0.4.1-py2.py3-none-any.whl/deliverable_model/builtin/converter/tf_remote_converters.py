from typing import Any

import numpy as np
import tensorflow as tf
from tensorflow_serving.apis.predict_pb2 import PredictRequest

from deliverable_model.converter_base import ConverterBase
from deliverable_model.request import Request
from deliverable_model.response import Response


class ConverterForRequest(ConverterBase):
    def call(self, request: Request) -> Any:
        predict_request = PredictRequest()
        predict_request.inputs["embedding_input"].CopyFrom(
            tf.make_tensor_proto(request.query, dtype=tf.float32)
        )
        return predict_request


class ConverterForResponse(ConverterBase):
    def call(self, response: Any) -> Response:
        tags_tensor_proto = response.outputs["crf"]
        tags_numpy = tf.make_ndarray(tags_tensor_proto)
        tags = tags_numpy.tolist()

        return Response(tags)
