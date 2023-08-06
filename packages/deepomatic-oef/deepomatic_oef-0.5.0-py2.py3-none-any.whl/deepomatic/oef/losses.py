from deepomatic.oef.protos import losses_pb2
from deepomatic.oef.utils import serializer


serializer.register_all(__name__, losses_pb2)
