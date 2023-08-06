from collections import namedtuple
from pathlib import Path
import copy

from deliverable_model.processor_base import ProcessorBase
from deliverable_model.request import Request
from deliverable_model.response import Response


PredictResult = namedtuple("PredictResult", ["sequence", "is_failed", "exec_msg"])


class BILUOEncodeProcessor(ProcessorBase):
    def __init__(self, decoder=None, **kwargs):
        super().__init__(**kwargs)

        self.decoder = decoder
        self.request_query = None

    @classmethod
    def load(cls, parameter: dict, asset_dir) -> "ProcessorBase":
        from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder

        decoder = BILUOSequenceEncoderDecoder()

        self = cls(decoder, **parameter)

        return self

    def preprocess(self, request: Request) -> Request:
        # record request for postprocess usage
        self.request_query = copy.deepcopy(request[self.pre_input_key])

        # don't change the request
        return request

    def postprocess(self, response: Response) -> Response:
        from tokenizer_tools.tagset.exceptions import TagSetDecodeError
        from tokenizer_tools.tagset.offset.sequence import Sequence

        tags_list = response[self.post_input_key]
        raw_text_list = self.request_query

        infer_result = []

        for raw_text, tags in zip(raw_text_list, tags_list):
            # decode Unicode
            tags_seq = [i.decode() if isinstance(i, bytes) else i for i in tags]

            # BILUO to offset
            is_failed = False
            exec_msg = None
            try:
                seq = self.decoder.to_offset(tags_seq, raw_text)
            except TagSetDecodeError as e:
                exec_msg = str(e)

                # invalid tag sequence will raise exception
                # so return a empty result to avoid batch fail
                seq = Sequence(raw_text)
                is_failed = True

            infer_result.append(PredictResult(seq, is_failed, exec_msg))

        response[self.post_output_key] = infer_result

        return response

    def get_dependency(self) -> list:
        return ["tokenizer_tools"]
