from pathlib import Path
from typing import List, Dict

from deliverable_model.processor_base import ProcessorBase
from deliverable_model.utils import get_class_fqn_name, create_dir_if_needed


class ProcessorHandle(object):
    """
    A object that present a processor instance already registered.
    """

    def __init__(self, processor_instance: str):
        self.processor_instance = processor_instance


class ProcessorBuilder(object):
    def __init__(self):
        self.processor_instance_registry: Dict[str, ProcessorBase] = {}
        self.preprocess_pipeline: List[str] = []
        self.postprocess_pipeline: List[str] = []
        self.dependency: List[str] = []
        self.build: bool = False

        self.processor_name_counter = {}

    def add_processor(self, processor: ProcessorBase) -> ProcessorHandle:
        processor_name = self._get_processor_key(processor)

        self.processor_instance_registry[processor_name] = processor

        return ProcessorHandle(processor_name)

    def _get_processor_key(self, processor) -> str:
        """
        get unique name for processor instance
        """
        processor_class = processor.__class__.__name__
        if processor_class not in self.processor_name_counter:
            self.processor_name_counter[processor_class] = 0

        current_count = self.processor_name_counter[processor_class]

        self.processor_name_counter[processor_class] += 1

        return "{}_{}".format(processor_class, current_count)

    def add_preprocess(self, processor: ProcessorHandle):
        """
        Add processor to preprocess pipeline, append to tail
        """
        self.preprocess_pipeline.append(processor.processor_instance)

    def add_postprocess(self, processor: ProcessorHandle, to_head=False):
        """
        Add processor to postprocess pipeline, append to head
        """
        if to_head:
            self.postprocess_pipeline.insert(0, processor.processor_instance)
        else:
            self.postprocess_pipeline.append(processor.processor_instance)

    def _gather_dependency(self) -> list:
        dependency = []
        for processor_instance in self.processor_instance_registry.values():
            dependency.extend(processor_instance.get_dependency())

        return list(sorted(set(dependency)))

    def save(self):
        self.dependency = self._gather_dependency()

        self.build = True

    def serialize(self, asset_dir: Path):
        instance = {}
        for (
            processor_instance_name,
            processor_instance,
        ) in self.processor_instance_registry.items():
            processor_instance_asset_dir = create_dir_if_needed(
                asset_dir / processor_instance_name
            )
            processor_instance.serialize(processor_instance_asset_dir)

            instance[processor_instance_name] = {
                "class": get_class_fqn_name(processor_instance),
                "parameter": processor_instance.get_config(),
            }

        pipeline = {"pre": self.preprocess_pipeline, "post": self.postprocess_pipeline}

        return {"version": "1.0", "instance": instance, "pipeline": pipeline}

    def get_dependency(self):
        return self.dependency
