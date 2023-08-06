from deliverable_model.serving.model.model_loaders.model_registry import (
    register_model_loader,
)

from deliverable_model.serving.model.model_loaders.keras_h5_model import KerasH5Model
from deliverable_model.serving.model.model_loaders.tensorflow_saved_model import (
    TensorFlowSavedModel,
)
from deliverable_model.serving.model.model_loaders.keras_saved_model import (
    KerasSavedModel,
)
from deliverable_model.serving.model.model_loaders.dummy_model import DummyModel

register_model_loader(KerasH5Model.name, KerasH5Model)
register_model_loader(TensorFlowSavedModel.name, TensorFlowSavedModel)
register_model_loader(KerasSavedModel.name, KerasSavedModel)
register_model_loader(DummyModel.name, DummyModel)
