from deepomatic.oef.utils import serializer
from deepomatic.oef.protos.models.image import preprocessing_pb2

serializer.register_all(__name__, preprocessing_pb2)
