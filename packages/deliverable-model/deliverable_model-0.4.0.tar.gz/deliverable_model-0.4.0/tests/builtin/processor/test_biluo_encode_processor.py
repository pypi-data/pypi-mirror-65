from deliverable_model.builtin.processor.biluo_decode_processor import (
    BILUOEncodeProcessor,
)
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.exceptions import TagSetDecodeError
from tokenizer_tools.tagset.offset.sequence import Sequence


def test_build(datadir, tmpdir):
    processor = BILUOEncodeProcessor()
    config = processor.serialize(tmpdir)
    print("config:", processor)
    pass
