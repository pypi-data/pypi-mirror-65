from pathlib import Path

import tensorflow as tf

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)


class KerasSavedModel(ModelLoaderBase):
    name = "keras_saved_model"

    @classmethod
    def load(cls, model_path: Path, metadata):
        model = tf.keras.experimental.load_from_saved_model(str(model_path))

        # patch for thread safety issue, but it seems don't work
        model._make_predict_function()

        self = cls(model.predict_on_batch)

        return self
