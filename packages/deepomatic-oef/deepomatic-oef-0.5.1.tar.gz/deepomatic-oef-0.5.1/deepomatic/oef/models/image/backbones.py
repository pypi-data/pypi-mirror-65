from deepomatic.oef.utils import serializer
from deepomatic.oef.protos.models.image import backbones_pb2

serializer.register_all(__name__, backbones_pb2)
