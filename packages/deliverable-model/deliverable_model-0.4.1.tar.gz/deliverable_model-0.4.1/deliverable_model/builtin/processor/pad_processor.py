from typing import Dict

from deliverable_model.processor_base import ProcessorBase
from deliverable_model.request import Request
from deliverable_model.response import Response


class PadProcessor(ProcessorBase):
    def __init__(self, padding_parameter=None, **kwargs):
        super().__init__(**kwargs)

        self.padding_parameter = (
            padding_parameter if padding_parameter is not None else {}
        )  # type: Dict[str, str]

    def get_config(self):
        config =  {"padding_parameter": self.padding_parameter}

        return {**super().get_config(), **config}

    @classmethod
    def load(cls, parameter: dict, asset_dir) -> "ProcessorBase":
        self = cls(**parameter)

        return self

    def add_padding_parameter(self, **kwargs):
        self.padding_parameter = kwargs

    def preprocess(self, request: Request) -> Request:
        import tensorflow as tf

        padded_query_id_list = tf.keras.preprocessing.sequence.pad_sequences(
            request[self.pre_input_key], **self.padding_parameter
        )

        request[self.pre_output_key] = padded_query_id_list

        return request

    def postprocess(self, response: Response) -> Response:
        # do nothing
        return response

    def get_dependency(self) -> list:
        return ["tensorflow"]
