from typing import Dict

from deliverable_model.processor_base import ProcessorBase
from deliverable_model.request import Request
from deliverable_model.response import Response


class StrTokensConvertProcessor(ProcessorBase):
    @classmethod
    def load(cls, parameter: dict, asset_dir) -> "ProcessorBase":
        self = cls(**parameter)

        return self

    def preprocess(self, request: Request) -> Request:
        request[self.pre_output_key] = [list(i) for i in request[self.pre_input_key]]

        return request

    def postprocess(self, response: Response) -> Response:
        # do nothing
        return response
