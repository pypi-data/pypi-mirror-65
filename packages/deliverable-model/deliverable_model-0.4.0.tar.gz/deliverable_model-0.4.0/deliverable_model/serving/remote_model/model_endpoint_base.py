from deliverable_model.request import Request
from deliverable_model.response import Response


class ModelEndpointBase:
    @classmethod
    def from_config(cls, *args, **kwargs):
        raise NotImplementedError

    def inference(self, request: Request) -> Response:
        raise NotImplementedError
