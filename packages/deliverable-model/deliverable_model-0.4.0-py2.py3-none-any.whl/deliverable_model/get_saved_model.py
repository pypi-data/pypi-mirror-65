import sys
from pathlib import Path

from deliverable_model.metacontent import MetaContent
from deliverable_model.serving.deliverable_model import DeliverableModel
from deliverable_model.serving.metadata.metadata import Metadata


def get_saved_model(model_path) -> str:
    model_path = Path(model_path)

    model_metadata = DeliverableModel._load_metadata(model_path)

    model_type = model_metadata["model"]["type"]

    if "saved_model" not in model_type:
        raise ValueError("Model is not a saved model")

    saved_model_path = model_path / "asset" / "model" / model_type

    return str(saved_model_path)


if __name__ == "__main__":
    saved_model_path = get_saved_model(sys.argv[1])
    print(saved_model_path)
