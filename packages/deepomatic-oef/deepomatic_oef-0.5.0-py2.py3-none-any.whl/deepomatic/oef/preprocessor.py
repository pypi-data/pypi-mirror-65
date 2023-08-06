from deepomatic.oef.protos import preprocessor_pb2
from deepomatic.oef.utils import serializer


serializer.register_all(__name__, preprocessor_pb2)
