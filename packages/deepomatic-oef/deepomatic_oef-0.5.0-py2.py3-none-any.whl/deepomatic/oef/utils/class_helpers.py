from enum import Enum
import importlib

serializer_class = None  # this is a small hack to delay the loading of the Serializer class to break an import loop (serializer.py loads class_helper)

api_prefix = 'deepomatic.oef.'
api_proto_prefix = api_prefix + 'protos.'
proto_suffix = '_pb2'

class ClassType(Enum):
    PROTO = api_proto_prefix
    API = api_prefix

# -----------------------------------------------------------------------------#

def split_path_into_module_and_class(path):
    """
    By convention, classes start with a capital letter and modules only have small letters.
    We use that to split a path into module and class
    """
    module = []
    classes = []
    path = path.split('.')
    for i, part in enumerate(path):
        if part[0].isupper():
            classes = path[i:]
            break
        module.append(part)
    module = '.'.join(module)
    return module, classes

# -----------------------------------------------------------------------------#

def get_normalized_module_and_classes(path):
    """
    Get the normalized (non back-end, without '_pb2') module name and class names from a path.
    E.g. deepomatic.oef.Model.SubClass would return ('model', ['Model', 'SubClass'])
    """

    # Be careful, the order of the if branch matters
    if path.startswith(api_proto_prefix):
        path = path.replace(api_proto_prefix, '')
        module, classes = split_path_into_module_and_class(path)
        if module.endswith(proto_suffix):
            module = module[:-len(proto_suffix)]
        return module, classes
    elif path.startswith(api_prefix):
        path = path.replace(api_prefix, '')
    else:
        raise Exception("Unexpected path type, does not start with any known prefix: '{}'".format(path))

    return split_path_into_module_and_class(path)

# -----------------------------------------------------------------------------#

def convert_module_path(path, to_type):
    """
    Takes a normalized module `path` and convert it to a specialized path of type `to_type`
    Args:
        path (string): a module path, normalized by get_normalized_module_and_classes
        to_type (ClassType): an enum of type ClassType

    Returns:
        string: The specialized module path.
    """
    path = to_type.value + path
    if to_type == ClassType.PROTO:
        path += proto_suffix
    return path

def convert_path(path, to_type):
    """Convert a package path from a ClassType to Another"""
    module, classes = get_normalized_module_and_classes(path)
    module = convert_module_path(module, to_type)
    return module, classes

# -----------------------------------------------------------------------------#

def load_class(module, classes, getter=getattr):
    """Load class from module path and a list of nested classes"""
    class_container = importlib.import_module(module)
    for c in classes:
        class_container = getter(class_container, c)
    return class_container

# -----------------------------------------------------------------------------#

def get_module_and_class_from_protobuf_descriptor(message):
    """
    Returns the package name without any prefix and the (eventually nested) classes
    E.g: deepomatic.oef.protos.models.image.Detection.TensorflowModelsMetaArchitecture would return
    (models.image, Detection.TensorflowModelsMetaArchitecture)
    """
    field_type = message.full_name
    assert field_type.startswith(api_prefix), "Field type should normally start with '{}'".format(api_prefix)
    field_type = field_type.replace(api_prefix, '')
    # Find the file holding the class that defines the field type and do a few checks
    package_name = message.file.name
    assert package_name.endswith('.proto'), "File type should normally end with '.proto'"
    package_name = package_name.replace('.proto', '').replace('/', '.')  # order matters for the replace
    assert package_name.startswith(api_proto_prefix), "Package should normally start with '{}'".format(api_proto_prefix)
    package_name = package_name.replace(api_proto_prefix, '')
    assert field_type.startswith(package_name), 'Protobuf malformation: the protobuf file does not starts with its package'
    field_type = field_type.replace(package_name + '.', '')
    return package_name, field_type

def load_proto_class_from_protobuf_descriptor(message, class_type=ClassType.PROTO, getter=getattr):
    module_path, classes = get_module_and_class_from_protobuf_descriptor(message)
    module_path = convert_module_path(module_path, class_type)
    return load_class(module_path, classes.split('.'), getter=getter)

# -----------------------------------------------------------------------------#
