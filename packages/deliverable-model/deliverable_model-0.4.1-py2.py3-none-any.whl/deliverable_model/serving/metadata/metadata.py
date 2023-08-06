from deliverable_model.metacontent import MetaContent


class Metadata(object):
    def __init__(self, metadata):
        self.metadata = metadata

    @classmethod
    def load(cls, model_path, metadata) -> "Metadata":
        self = cls(metadata)

        return self

    def get_meta_content(self) -> MetaContent:
        return MetaContent(self.metadata["id"])
