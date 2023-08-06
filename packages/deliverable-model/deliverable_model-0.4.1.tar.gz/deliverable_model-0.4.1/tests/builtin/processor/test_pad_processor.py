from deliverable_model.builtin.processor.pad_processor import PadProcessor


def test_build(datadir, tmpdir):
    padProcessor = PadProcessor()
    param = {"a": "fish", "b": "bird", "c": "panda"}
    padProcessor.add_padding_parameter(params=param)
    config = padProcessor.get_config()
    expect = {"padding_parameter": {"params": {"a": "fish", "b": "bird", "c": "panda"}}}
    assert expect == config
    padProcessor.serialize(tmpdir)
