import grpc
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis.predict_pb2 import PredictRequest
from deliverable_model.serving.model import Model
from deliverable_model.request import Request
from deliverable_model.response import Response
from deliverable_model.serving.model.model_endpoint_base import ModelEndpointBase


class TFServingModelEndpoint(ModelEndpointBase):
    def __init__(
        self,
        target: str,
        model_name,
        signature_name,
        request_converter,
        response_converter,
    ):
        self.model_name = model_name
        self.signature_name = signature_name

        self.channel = grpc.insecure_channel(target)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

        self.request_converter = request_converter
        self.response_converter = response_converter

    @classmethod
    def load(
        cls,
        target,
        model_name,
        signature_name="serving_default",
        converter_for_request=None,
        converter_for_response=None,
    ):
        # TODO(howl-anderson): converter should not be part of endpoint instance,
        # _make_request because every endpoint instance share same converter loader
        request_converter = Model._load_converter(converter_for_request)
        response_converter = Model._load_converter(converter_for_response)

        self = cls(
            target, model_name, signature_name, request_converter, response_converter
        )

        return self

    def inference(self, request: Request) -> Response:
        predict_request = self.request_converter(request)

        feature = self.stub.Predict(predict_request, 5.0)

        response = self.response_converter(feature)

        return response

    def _make_request(self, request: Request) -> PredictRequest:
        pred_request = PredictRequest()
        pred_request.model_spec.name = self.model_name
        pred_request.model_spec.signature_name = self.signature_name

        for k, v in request.query.items():
            request.inputs[k].CopyFrom(tf.make_tensor_proto(v))

        return pred_request

    def _make_response(self, response: Any) -> Response:
        tags_tensor_proto = response.outputs["tags"]
        tags_numpy = tf.make_ndarray(tags_tensor_proto)
        unicode_tags_numpy = np.vectorize(lambda x: x.decode())(tags_numpy)
        tags = unicode_tags_numpy.tolist()

        response = Response(tags)
        return response


if __name__ == "__main__":
    tfse = TFServingModelEndpoint.load("127.0.0.1:5000", "ner")
    request = Request(["明天的天气", "播放歌曲"])
    tfse.inference(request)
