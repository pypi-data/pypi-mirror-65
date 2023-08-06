import filecmp

from deliverable_model.builder.processor.processor_builder import ProcessorBuilder
from deliverable_model.builtin.processor.lookup_processor import LookupProcessor
from seq2annotation.input import Lookuper


def test_build(datadir, tmpdir):
    processor_builder = ProcessorBuilder()

    # setup test processor
    lookup_processor = LookupProcessor()

    vocabulary_lookup_table = Lookuper({"a": 1, "b": 2, "c": 3})
    lookup_processor.add_vocabulary_lookup_table(vocabulary_lookup_table)

    tag_lookup_table = Lookuper({"tag-a": 1, "tag-b": 2, "tag-c": 3})
    lookup_processor.add_tag_lookup_table(tag_lookup_table)

    lookup_processor_handle = processor_builder.add_processor(lookup_processor)
    processor_builder.add_preprocess(lookup_processor_handle)
    processor_builder.add_postprocess(lookup_processor_handle)

    processor_builder.save()

    config = processor_builder.serialize(tmpdir)

    dircmp_obj = filecmp.dircmp(datadir, tmpdir)

    assert not dircmp_obj.diff_files

    assert config == {
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
    }

    assert processor_builder.get_dependency() == ["seq2annotation"]
