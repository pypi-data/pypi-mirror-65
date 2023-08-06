import grpc
from typing import Any
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis.predict_pb2 import PredictRequest
from deliverable_model.request import Request
from deliverable_model.response import Response
from deliverable_model.serving.remote_model.model_endpoint_base import ModelEndpointBase
from deliverable_model.serving.remote_model.model_registry import register_model_loader


class TFServingModelEndpoint(ModelEndpointBase):
    name = "tf+grpc"

    def __init__(self, target: str, model_name, signature_name):
        self.model_name = model_name
        self.signature_name = signature_name

        self.channel = grpc.insecure_channel(target)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

    @classmethod
    def load(cls, target, model_name, signature_name="serving_default"):
        self = cls(target, model_name, signature_name)

        return self

    @classmethod
    def from_config(cls, metadata, config):
        return cls.load(**config)

    def inference(self, request: PredictRequest) -> Any:
        request.model_spec.name = self.model_name
        request.model_spec.signature_name = self.signature_name

        feature = self.stub.Predict(request, 5.0)

        return feature


if __name__ == "__main__":
    tfse = TFServingModelEndpoint.load("127.0.0.1:5000", "ner")
    request = Request(["明天的天气", "播放歌曲"])
    tfse.inference(request)
