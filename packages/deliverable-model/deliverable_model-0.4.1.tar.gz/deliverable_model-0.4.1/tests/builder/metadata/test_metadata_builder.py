from deliverable_model.builder.metadata.metadata_builder import MetadataBuilder
from deliverable_model.metacontent import MetaContent

# python intergrated tools
def test_build(datadir, tmpdir):
    metadata_builder = MetadataBuilder()

    meta_content = MetaContent("algorithmId-corpusId-configId-runId")

    metadata_builder.set_meta_content(meta_content)

    metadata_builder.save()

    assert metadata_builder.build == True

    config = metadata_builder.serialize(None)

    assert config == {"version": "1.0", "id": "algorithmId-corpusId-configId-runId"}

    assert metadata_builder.get_dependency() == []
