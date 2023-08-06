import filecmp

from deliverable_model.builder.deliverable_model_builder import DeliverableModelBuilder
from deliverable_model.builder.metadata.metadata_builder import MetadataBuilder
from deliverable_model.builder.model.model_builder import ModelBuilder
from deliverable_model.builder.processor.processor_builder import ProcessorBuilder
from deliverable_model.builtin.processor.lookup_processor import LookupProcessor
from deliverable_model.metacontent import MetaContent
from seq2annotation.input import Lookuper


def test_build(datadir, tmpdir):
    deliverable_model_builder = DeliverableModelBuilder(tmpdir)

    # metadata builder
    metadata_builder = MetadataBuilder()

    meta_content = MetaContent("algorithmId-corpusId-configId-runId")

    metadata_builder.set_meta_content(meta_content)

    metadata_builder.save()

    # processor builder
    processor_builder = ProcessorBuilder()

    lookup_processor = LookupProcessor()

    vocabulary_lookup_table = Lookuper({"a": 1, "b": 2, "c": 3})
    lookup_processor.add_vocabulary_lookup_table(vocabulary_lookup_table)

    tag_lookup_table = Lookuper({"tag-a": 1, "tag-b": 2, "tag-c": 3})
    lookup_processor.add_tag_lookup_table(tag_lookup_table)

    lookup_processor_handle = processor_builder.add_processor(lookup_processor)
    processor_builder.add_preprocess(lookup_processor_handle)
    processor_builder.add_postprocess(lookup_processor_handle)

    processor_builder.save()

    # model builder
    model_builder = ModelBuilder()
    model_builder.add_keras_h5_model(datadir / "fixture" / "keras_h5_model")
    model_builder.save()

    #
    deliverable_model_builder.add_processor(processor_builder)
    deliverable_model_builder.add_metadata(metadata_builder)
    deliverable_model_builder.add_model(model_builder)

    metadata = deliverable_model_builder.save()

    assert metadata == {
        "version": "1.0",
        "dependency": ["seq2annotation", "tensorflow"],
        "processor": {
            "version": "1.0",
            "instance": {
                "LookupProcessor_0": {
                    "class": "deliverable_model.builtin.processor.lookup_processor.LookupProcessor",
                    "parameter": {
                        "lookup_table": ["vocabulary", "tag"],
                        "padding_parameter": {},
                    },
                }
            },
            "pipeline": {"pre": ["LookupProcessor_0"], "post": ["LookupProcessor_0"]},
        },
        "model": {
            "version": "1.0",
            "type": "keras_h5_model",
            "custom_object_dependency": [],
            "converter_for_request": {
                "class_name": "deliverable_model.builder.model.model_builder.SimpleConverterForRequest",
                "config": {},
            },
            "converter_for_response": {
                "class_name": "deliverable_model.builder.model.model_builder.SimpleConverterForResponse",
                "config": {},
            },
        },
        "metadata": {"version": "1.0", "id": "algorithmId-corpusId-configId-runId"},
    }

    #
    dircmp_obj = filecmp.dircmp(datadir / "expected", tmpdir)
    assert not dircmp_obj.diff_files
