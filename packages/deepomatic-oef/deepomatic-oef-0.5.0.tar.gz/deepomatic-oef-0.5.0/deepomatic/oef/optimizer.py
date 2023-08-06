from deepomatic.oef.protos import optimizer_pb2
from deepomatic.oef.utils import serializer


serializer.register_all(__name__, optimizer_pb2)
