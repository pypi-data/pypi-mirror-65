from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import model_pb2

class Model(serializer.Serializer):
    """An model object

    Keyword arguments:
    input_data_tensor_mapping -- a map from model tensors to dataset input data (optionnal)
    annotation_tensor_mapping -- a map from model tensors to dataset annotations (optionnal)
    """
    optional_fields = ['input_data_tensor_mapping', 'annotation_tensor_mapping']


serializer.register_all(__name__, model_pb2)
