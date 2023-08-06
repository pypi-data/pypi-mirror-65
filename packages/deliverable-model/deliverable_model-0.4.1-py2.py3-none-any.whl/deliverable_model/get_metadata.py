from pathlib import Path

from deliverable_model.serving.deliverable_model import DeliverableModel
from deliverable_model.metacontent import MetaContent
from deliverable_model.serving.metadata.metadata import Metadata


def get_metadata(model_path) -> MetaContent:
    model_path = Path(model_path)

    model_metadata = DeliverableModel._load_metadata(model_path)

    metadata_object = Metadata.load(
        model_path / "asset" / "metadata", model_metadata["metadata"]
    )

    return metadata_object.get_meta_content()
