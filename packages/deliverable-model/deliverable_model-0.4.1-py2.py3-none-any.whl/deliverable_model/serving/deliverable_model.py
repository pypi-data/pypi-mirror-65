import json
import subprocess
import sys
from pathlib import Path
from typing import Dict

from deliverable_model.metacontent import MetaContent
from deliverable_model.serving.metadata.metadata import Metadata
from deliverable_model.serving.model.model import Model
from deliverable_model.serving.remote_model.remote_model import RemoteModel
from deliverable_model.serving.processor.processor import Processor
from deliverable_model.request import Request
from deliverable_model.response import Response


class DeliverableModel(object):
    def __init__(self, model_path: Path, model_metadata: Dict):
        self.model_path = model_path
        self.model_metadata = model_metadata

        self.processor_object = None  # type: Processor
        self.model_object = None  # type: Model
        self.metadata_object = None  # type: Metadata

    @classmethod
    def load(cls, model_path, model_endpoint=None) -> "DeliverableModel":
        model_path = Path(model_path)
        model_metadata = cls._load_metadata(model_path)

        cls._check_compatible(model_metadata)

        cls._install_dependency(model_metadata)

        self = cls(model_path, model_metadata)

        self._instance_processor()

        if model_endpoint is None:
            # local model
            self._instance_model()
        else:
            # remote model
            self._instance_remote_model(model_endpoint)

        self._instance_metadata()

        return self

    @classmethod
    def _load_metadata(cls, model_path: Path) -> Dict:
        metadata_file = model_path / "metadata.json"
        with metadata_file.open("rt") as fd:
            metadata = json.load(fd)

        return metadata

    @classmethod
    def _check_compatible(cls, metadata):
        """
        check if version is compatible

        if check pass nothing happen, otherwise raise a exception
        """
        # TODO(howl-anderson): implement this
        pass

    @classmethod
    def _install_dependency(cls, metadata):
        """
        install python packages according to metadata

        if install failed, an exception will raise.
        """
        for dependency in metadata["dependency"]:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])

    def inference(self, request: Request) -> Response:
        request = self._call_preprocessor(request)
        response = self._call_model(request)
        response = self._call_postprocessor(response)

        return response

    def metadata(self) -> MetaContent:
        return self.metadata_object.get_meta_content()

    def _instance_processor(self):
        self.processor_object = Processor.load(
            self.model_path / "asset" / "processor", self.model_metadata["processor"]
        )

    def _instance_model(self):
        self.model_object = Model.load(
            self.model_path / "asset" / "model", self.model_metadata["model"]
        )

    def _instance_remote_model(self, endpoint_config):
        self.model_object = RemoteModel.load(
            self.model_metadata["remote_model"], endpoint_config
        )

    def _instance_metadata(self):
        self.metadata_object = Metadata.load(
            self.model_path / "asset" / "metadata", self.model_metadata["metadata"]
        )

    def _call_preprocessor(self, request: Request) -> Request:
        return self.processor_object.call_preprocessor(request)

    def _call_model(self, request: Request) -> Response:
        return self.model_object.inference(request)

    def _call_postprocessor(self, response: Response) -> Response:
        return self.processor_object.call_postprocessor(response)
