from . import class_helpers

from deepomatic.oef.protos.models.image_pb2 import Detection as DetectionProto
from deepomatic.oef.models.image import Detection as DetectionAPI

def test_split_path_into_module_and_class():
    assert class_helpers.split_path_into_module_and_class('thoth.core.backends.tensorflow.model.Model.SubClass') == ('thoth.core.backends.tensorflow.model', ['Model', 'SubClass'])

def test_get_normalized_module_and_classes():
    assert class_helpers.get_normalized_module_and_classes('deepomatic.oef.model.Model') == ('model', ['Model'])
    assert class_helpers.get_normalized_module_and_classes('deepomatic.oef.model.Model.SubClass') == ('model', ['Model', 'SubClass'])
    assert class_helpers.get_normalized_module_and_classes('deepomatic.oef.model') == ('model', [])
    assert class_helpers.get_normalized_module_and_classes('deepomatic.oef.model') == ('model', [])
    assert class_helpers.get_normalized_module_and_classes('deepomatic.oef.protos.model.Model') == ('model', ['Model'])
    assert class_helpers.get_normalized_module_and_classes('deepomatic.oef.protos.model_pb2') == ('model', [])

def test_convert_module_path():
    assert class_helpers.convert_module_path('model', class_helpers.ClassType.API) == 'deepomatic.oef.model'
    assert class_helpers.convert_module_path('models.image', class_helpers.ClassType.PROTO) == 'deepomatic.oef.protos.models.image_pb2'

def test_convert_path():
    assert class_helpers.convert_path('deepomatic.oef.model.Model.SubClass', class_helpers.ClassType.API) == ('deepomatic.oef.model', ['Model', 'SubClass'])
    assert class_helpers.convert_path('deepomatic.oef.model', class_helpers.ClassType.PROTO) == ('deepomatic.oef.protos.model_pb2', [])

def test_load_class():
    assert class_helpers.load_class('deepomatic.oef.protos.models.image_pb2', ['Detection']) == DetectionProto
    assert class_helpers.load_class('deepomatic.oef.protos.models.image_pb2', ['Detection', 'TensorflowModelsMetaArchitecture']) == DetectionProto.TensorflowModelsMetaArchitecture
    assert class_helpers.load_class('deepomatic.oef.models.image', ['Detection']) == DetectionAPI
