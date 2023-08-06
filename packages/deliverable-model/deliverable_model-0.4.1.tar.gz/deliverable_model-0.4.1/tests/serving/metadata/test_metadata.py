from deliverable_model.serving.metadata.metadata import Metadata
from deliverable_model.metacontent import MetaContent


def test_serving():
    metadata_obj = Metadata.load(
        None, {"version": "1.0", "id": "algorithmId-corpusId-configId-runId"}
    )

    assert metadata_obj.get_meta_content() == MetaContent(
        "algorithmId-corpusId-configId-runId"
    )
