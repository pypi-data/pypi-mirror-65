from typing import Any

import numpy as np
import tensorflow as tf
from micro_toolkit.data_process.text_sequence_padding import TextSequencePadding
from tensorflow_serving.apis.predict_pb2 import PredictRequest

from deliverable_model.converter_base import ConverterBase
from deliverable_model.response import Response
from deliverable_model.request import Request
from deliverable_model.response import Response


class ConverterForRequest(ConverterBase):
    def call(self, request: Request) -> Any:

        tsp = TextSequencePadding("<pad>")
        return {
            "words": tsp.fit(request.query),
            "words_len": [
                len(list(filter(lambda x: x != 0.0, text))) for text in request.query
            ],
        }


class ConverterForResponse(ConverterBase):
    def call(self, response: Any) -> Response:

        return Response(response["tags"])


class RemoteKerasConverterForRequest(ConverterBase):
    def call(self, request: Request) -> Any:
        predict_request = PredictRequest()
        predict_request.inputs["embedding_input"].CopyFrom(
            tf.make_tensor_proto(request.query, dtype=tf.float32)
        )
        return predict_request


class RemoteKerasConverterForResponse(ConverterBase):
    def call(self, response: Any) -> Response:
        tags_tensor_proto = response.outputs["crf"]
        tags_numpy = tf.make_ndarray(tags_tensor_proto)
        tags = tags_numpy.tolist()

        return Response(tags)


class RemoteEstimatorConverterForRequest(ConverterBase):
    def call(self, request: Request) -> Any:

        tsp = TextSequencePadding("<pad>")
        data = {
            "words": tsp.fit(request.query),
            "words_len": [
                len(list(filter(lambda x: x != 0.0, text))) for text in request.query
            ],
        }

        predict_request = PredictRequest()
        predict_request.inputs["words"].CopyFrom(
            tf.make_tensor_proto(data["words"], dtype=tf.string)
        )
        predict_request.inputs["words_len"].CopyFrom(
            tf.make_tensor_proto(data["words_len"], dtype=tf.int32)
        )
        return predict_request


class RemoteEstimatorConverterForResponse(ConverterBase):
    def call(self, response: Any) -> Response:
        tags_tensor_proto = response.outputs["tags"]
        tags_numpy = tf.make_ndarray(tags_tensor_proto)
        tags = tags_numpy.tolist()

        return Response(tags)
