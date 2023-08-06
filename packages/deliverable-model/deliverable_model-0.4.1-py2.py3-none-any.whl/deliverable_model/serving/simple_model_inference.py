from typing import Union, List, Iterator, Dict

from tqdm import tqdm

from deliverable_model.metacontent import MetaContent
from deliverable_model.builtin.processor.biluo_decode_processor import PredictResult
from micro_toolkit.data_process.batch_iterator import BatchingIterator

from deliverable_model.request import Request
from deliverable_model.serving import DeliverableModel


class SimpleModelInference:
    def __init__(self, model_dir, batch_size=1):
        self.batch_size = batch_size

        self.server = DeliverableModel.load(model_dir)

    def _parse(self, msg):
        if not isinstance(msg, list) or not isinstance(msg[0], list):
            msg = [[j for j in i] for i in msg]

        request_obj = Request(msg)

        response_obj = self.server.parse(request_obj)

        for predict_info in response_obj.data:
            yield predict_info

    def parse(
        self, msg_list: Union[List[str], List[List[str]]]
    ) -> Iterator[PredictResult]:
        bi = BatchingIterator(self.batch_size)
        for i in tqdm(bi(msg_list), disable=None):
            for j in self._parse(i):
                yield j

    @property
    def model_metadata(self) -> Dict:
        return self.server.model_metadata

    @property
    def metadata(self) -> MetaContent:
        return self.server.metadata()
