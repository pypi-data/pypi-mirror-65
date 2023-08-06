from deepomatic.oef.protos.models import image_pb2
from deepomatic.oef.utils import serializer


serializer.register_all(__name__, image_pb2)
