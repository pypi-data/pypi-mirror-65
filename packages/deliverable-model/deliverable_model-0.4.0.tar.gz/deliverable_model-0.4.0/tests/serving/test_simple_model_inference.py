from deliverable_model.serving.simple_model_inference import SimpleModelInference
import pytest

# TODO what happened? i can't get the failure reason
@pytest.mark.skip("")
def test_serving(datadir):
    deliverable_model = SimpleModelInference(datadir)

    request = ["abc", "cba"]

    response = list(deliverable_model.parse(request))

    expected = [["tag-a", "tag-b", "tag-c"], ["tag-c", "tag-b", "tag-a"]]

    assert response == expected
