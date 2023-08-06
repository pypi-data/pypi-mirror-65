from deliverable_model.request import Request


def make_request(**kwargs) -> Request:
    return Request(**kwargs)
