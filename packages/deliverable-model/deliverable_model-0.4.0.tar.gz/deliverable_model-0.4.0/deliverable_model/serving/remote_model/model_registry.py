from pathlib import Path

from deliverable_model.serving.remote_model.model_endpoint_base import ModelEndpointBase

_endpoint_type_registry = {}


def get_endpoint_class_by_type(model_type) -> ModelEndpointBase:
    global _endpoint_type_registry

    model_loader_class = _endpoint_type_registry[model_type]
    return model_loader_class


def get_endpoint_instance_by_type(model_type, metadata, config) -> ModelEndpointBase:
    endpoint_class = get_endpoint_class_by_type(model_type)

    model_load_func = getattr(endpoint_class, "from_config")

    model_loader_instance = model_load_func(metadata, config)

    return model_loader_instance


def register_model_loader(model_type, model_loader_class: ModelEndpointBase):
    global _endpoint_type_registry

    if model_loader_class in _endpoint_type_registry:
        raise ValueError()
    _endpoint_type_registry[model_type] = model_loader_class
