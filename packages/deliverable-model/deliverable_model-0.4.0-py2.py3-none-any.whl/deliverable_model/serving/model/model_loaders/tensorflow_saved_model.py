from pathlib import Path
from typing import Union

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)


class TensorFlowSavedModel(ModelLoaderBase):
    name = "tensorflow_saved_model"

    @classmethod
    def load(cls, model_path: Path, metadata):
        # TODO(howl-anderson): contrib is not available at TF 2.x and TF enterprise,
        # find alternative for `predictor`
        from tensorflow.contrib import predictor

        concrete_model_path = cls._get_model(model_path)

        predictor_func = predictor.from_saved_model(str(concrete_model_path))

        self = cls(predictor_func)

        return self

    @classmethod
    def _get_model(cls, model_path: Path) -> Path:
        return cls._find_most_recent_model(model_path)

    @staticmethod
    def _find_most_recent_model(model_path: Path) -> Path:
        """
        find most recent model by directory name.

        In saved model, model directories are named after export date-time,
        such like `202002280029`.
        """

        def get_version(model_path: Path) -> Union[int, None]:
            dir_name = model_path.name
            if dir_name.isnumeric():
                return int(dir_name)

            return None

        most_recent_model_path = None
        most_recent_version = -1
        for candidate_path in model_path.iterdir():
            # skip none numeric path
            if not candidate_path.name.isnumeric():
                continue
            if not candidate_path.is_dir():
                continue

            if most_recent_model_path is None:
                most_recent_model_path = candidate_path

                continue

            # if candidate_path newer then current one
            candidate_version = get_version(candidate_path)
            if candidate_version > most_recent_version:
                most_recent_version = candidate_version
                most_recent_model_path = candidate_path

        return most_recent_model_path
