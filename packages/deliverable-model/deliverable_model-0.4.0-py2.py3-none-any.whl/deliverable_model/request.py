from typing import List, Any


class Request(dict):
    """
    Represent a list of request object
    """

    def __init__(self, query: List[Any]):
        self.query_history = []
        self["data"] = query

    @property
    def query(self):
        return self["data"]

    @query.setter
    def query(self, data):
        self["data"] = data

    def update_query(self, query):
        self.query_history.append(self.query)
        self["data"] = query
