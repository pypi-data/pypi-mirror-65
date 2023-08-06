from collections import Callable
from typing import Any


class ModelLoaderBase(object):
    name = None

    def __init__(self, predictor_func: Callable):
        self.predictor_func = predictor_func

    @classmethod
    def load(cls, model_path, metadata) -> "ModelLoaderBase":
        raise NotImplementedError

    def inference(self, request: Any) -> Any:
        predict_result = self.predictor_func(request)
        return predict_result
