from pathlib import Path

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)

_model_registry = {}


def get_model_loader_class_by_type(model_type) -> ModelLoaderBase:
    global _model_registry

    model_loader_class = _model_registry[model_type]
    return model_loader_class


def get_model_loader_instance_by_type(
    model_type, asset_dir: Path, metadata
) -> ModelLoaderBase:
    model_loader_class = get_model_loader_class_by_type(model_type)

    model_path = asset_dir / model_type

    model_load_func = getattr(model_loader_class, "load")

    model_loader_instance = model_load_func(model_path, metadata)

    return model_loader_instance


def register_model_loader(model_type, model_loader_class: ModelLoaderBase):
    global _model_registry

    if model_loader_class in _model_registry:
        raise ValueError()
    _model_registry[model_type] = model_loader_class
