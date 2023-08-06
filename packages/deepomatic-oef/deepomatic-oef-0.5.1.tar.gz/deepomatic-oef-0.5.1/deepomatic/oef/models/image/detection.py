from deepomatic.oef.utils import serializer
from deepomatic.oef.protos.models.image import detection_pb2

serializer.register_all(__name__, detection_pb2)
