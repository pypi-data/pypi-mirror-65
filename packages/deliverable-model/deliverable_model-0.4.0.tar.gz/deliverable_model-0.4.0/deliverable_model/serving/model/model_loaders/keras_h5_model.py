from pathlib import Path

import tensorflow as tf

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)


class KerasH5Model(ModelLoaderBase):
    name = "keras_h5_model"

    @classmethod
    def load(cls, model_path: Path, metadata):
        # TODO: not test at all
        model = tf.keras.models.load_model(str(model_path))

        # patch for thread safety issue, but it seems don't work
        model._make_predict_function()

        self = cls(model.predict_on_batch)

        return self
