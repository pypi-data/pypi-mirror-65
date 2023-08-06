from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import dataoperation_pb2

serializer.register_all(__name__, dataoperation_pb2)
