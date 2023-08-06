from deepomatic.oef.utils import serializer
from deepomatic.oef.protos.models.image import ocr_pb2

serializer.register_all(__name__, ocr_pb2)
