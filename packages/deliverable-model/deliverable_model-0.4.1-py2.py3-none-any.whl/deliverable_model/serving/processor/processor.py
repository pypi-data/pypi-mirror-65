from pathlib import Path

from deliverable_model.request import Request
from deliverable_model.response import Response
from deliverable_model.utils import class_from_module_path


class Processor(object):
    def __init__(self, asset_dir: Path, metadata):
        self.asset_dir = asset_dir
        self.metadata = metadata

        self.processor_instance = {}

    @classmethod
    def load(cls, model_path, metadata) -> "Processor":
        self = cls(model_path, metadata)

        self.instance_processor()

        return self

    def instance_processor(self):
        for instance_name, instance_build_info in self.metadata["instance"].items():
            processor_instance = self._instance_single_processor(
                instance_name, instance_build_info
            )

            self.processor_instance[instance_name] = processor_instance

    def _instance_single_processor(self, instance_name, instance_build_info):
        class_ = class_from_module_path(instance_build_info["class"])
        parameter = instance_build_info.get("parameter", {})

        class_load_method = getattr(class_, "load")

        instance_asset_dir = self.asset_dir / instance_name

        processor_instance = class_load_method(
            parameter=parameter, asset_dir=instance_asset_dir
        )

        return processor_instance

    def call_preprocessor(self, request: Request) -> Request:
        for processor_instance_name in self.metadata["pipeline"]["pre"]:
            processor_instance = self.processor_instance[processor_instance_name]
            preprocessor_method = getattr(processor_instance, "preprocess")
            request = preprocessor_method(request)

        return request

    def call_postprocessor(self, response: Response) -> Response:
        for processor_instance_name in self.metadata["pipeline"]["post"]:
            processor_instance = self.processor_instance[processor_instance_name]
            preprocessor_method = getattr(processor_instance, "postprocess")
            response = preprocessor_method(response)

        return response
