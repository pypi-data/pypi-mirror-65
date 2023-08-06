class MetaContent(object):
    def __init__(self, id_):
        self.id = id_

    def __eq__(self, other):
        return self.id == other.id
