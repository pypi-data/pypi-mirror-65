from pathlib import Path

from deliverable_model.request import Request
from deliverable_model.response import Response


class ProcessorBase(object):
    def __init__(self, **kwargs):
        self.input_key = "data"
        self.output_key = "data"

        self.pre_input_key = kwargs.get("pre_input_key", self.input_key)
        self.pre_output_key = kwargs.get("pre_output_key", self.output_key)
        self.post_input_key = kwargs.get("post_input_key", self.input_key)
        self.post_output_key = kwargs.get("post_output_key", self.output_key)

    def get_config(self):
        return {
            "pre_input_key": self.pre_input_key,
            "pre_output_key": self.pre_output_key,
            "post_input_key": self.post_input_key,
            "post_output_key": self.post_output_key,
        }

    def load(self, parameter: dict, asset_dir: Path) -> "ProcessorBase":
        raise NotImplementedError

    def preprocess(self, request: Request) -> Request:
        raise NotImplementedError

    def postprocess(self, response: Response) -> Response:
        raise NotImplementedError

    def serialize(self, asset_dir: Path):
        pass

    def get_dependency(self) -> list:
        return []
