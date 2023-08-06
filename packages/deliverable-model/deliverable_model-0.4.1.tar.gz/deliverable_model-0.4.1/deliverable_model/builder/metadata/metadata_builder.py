from deliverable_model.metacontent import MetaContent


class MetadataBuilder(object):
    version = "1.0"

    def __init__(self):
        self.id = None  # type: (str, str)
        self.dependency = []
        self.build = False

    def set_meta_content(self, meta_content: MetaContent):
        self.id = meta_content.id

    def save(self):
        self.build = True

    def serialize(self, export_dir):
        return {"version": self.version, "id": self.id}

    def get_dependency(self):
        return self.dependency
