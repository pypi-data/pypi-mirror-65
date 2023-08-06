from typing import Any

from deliverable_model.converter_base import ConverterBase
from deliverable_model.request import Request
from deliverable_model.response import Response


class ConverterForRequest(ConverterBase):
    def call(self, request: Request) -> Any:
        return request.query


class ConverterForResponse(ConverterBase):
    def call(self, response: Any) -> Response:
        return Response(response)
