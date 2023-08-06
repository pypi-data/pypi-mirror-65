import grpc
import tensorflow as tf
import numpy as np

from tensorflow_serving.apis import prediction_service_pb2_grpc
from tensorflow_serving.apis.predict_pb2 import PredictRequest

channel = grpc.insecure_channel("localhost:8500")

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


def main(words, words_len):
    request = PredictRequest()
    request.model_spec.name = "estimator_ner"
    request.model_spec.signature_name = "serving_default"
    request.inputs["words"].CopyFrom(tf.make_tensor_proto(words))
    request.inputs["words_len"].CopyFrom(tf.make_tensor_proto(words_len))

    feature = stub.Predict(request, 5.0)
    return feature


if __name__ == "__main__":
    from tqdm import tqdm

    for _ in tqdm(range(10000)):
        result = main(
            [
                ["播", "放", "周", "杰", "伦", "的", "七", "里", "香"],
                ["导", "航", "去", "徐", "家", "汇", "<pad>", "<pad>", "<pad>"],
            ],
            [9, 6],
        )

        tags_tensor_proto = result.outputs["tags"]
        tags_numpy = tf.make_ndarray(tags_tensor_proto)
        unicode_tags_numpy = np.vectorize(lambda x: x.decode())(tags_numpy)
        tags = unicode_tags_numpy.tolist()

        # print(tags)
