from pathlib import Path
from typing import Callable

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)
from deliverable_model.request import Request
from deliverable_model.response import Response


class DummyModel(ModelLoaderBase):
    name = "dummy_model"

    def __init__(self, predictor_func: Callable):
        self.predictor_func = predictor_func

    @classmethod
    def load(cls, model_path: Path, metadata):
        data_file = model_path / "data"

        with data_file.open("rt") as fd:
            add_num = int(fd.read())

        def predict_func(data):
            # element wide add add_num
            new_data = []
            for example in data:
                new_example = []
                for item in example:
                    new_item = item + add_num
                    new_example.append(new_item)

                new_data.append(new_example)

            return new_data

        self = cls(predict_func)

        return self

    def inference(self, request: Request) -> Response:
        result = self.predictor_func(request.query)

        response = Response(result)

        return response
