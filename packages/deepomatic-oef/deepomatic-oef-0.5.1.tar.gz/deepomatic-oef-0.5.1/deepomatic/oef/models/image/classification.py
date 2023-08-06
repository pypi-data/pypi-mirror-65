from deepomatic.oef.utils import serializer
from deepomatic.oef.protos.models.image import classification_pb2

serializer.register_all(__name__, classification_pb2)
