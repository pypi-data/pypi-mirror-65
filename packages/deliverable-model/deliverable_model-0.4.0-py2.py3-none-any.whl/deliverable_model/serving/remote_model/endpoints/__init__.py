from deliverable_model.serving.remote_model.model_registry import register_model_loader
from deliverable_model.serving.remote_model.endpoints.tf_serving_model_endpoint import (
    TFServingModelEndpoint,
)

__all__ = ["TFServingModelEndpoint"]

register_model_loader(TFServingModelEndpoint.name, TFServingModelEndpoint)
