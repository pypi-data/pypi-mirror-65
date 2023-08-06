import deliverable_model.serving.model  # for auto registry
import deliverable_model.serving.remote_model  # for auto registry
from deliverable_model.serving.deliverable_model import DeliverableModel
from deliverable_model.serving.make_endpoint_config import make_endpoint_config
from deliverable_model.serving.make_request import make_request

load = DeliverableModel.load
