import inspect
import logging
from google.protobuf.descriptor import FieldDescriptor
import google.protobuf.json_format as json_format
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType

from deepomatic.oef.utils import class_helpers
from deepomatic.oef.utils.common import parse_protobuf_from_json_or_binary

module_prefix = __name__.split('.')[0] + '.'

logger = logging.getLogger(__name__)

class SerializerException(Exception):
    pass


def assert_between_0_and_x(s, field_name, x=1.):
    value = getattr(s, field_name)
    if value < 0. or value > x:
        raise SerializerException("Field should be between 0 and {}: {}".format(x, field_name))


def assert_non_empty(s, field_name):
    value = getattr(s, field_name)
    if len(value) == 0:
        raise SerializerException("Field should be non empty: {}".format(field_name))


def get_non_none_keys(kwargs):
        return set(map(lambda kv: kv[0], filter(lambda kv: kv[1] is not None, kwargs.items())))


def get_value_key(prefix, key):
    return prefix + '.{}'.format(key)


###############################################################################

def is_array(msg, field_name):
    field = getattr(msg, field_name)
    return getattr(field, 'extend', None) is not None


def is_map(msg, field_name):
    field = getattr(msg, field_name)
    return getattr(field, 'get_or_create', None) is not None


###############################################################################

def get_or_create_serializer_class_from_protobuf_descriptor(message):
    def get_or_create_serializer(container_class, class_name):
        package_name = inspect.getfile(container_class)
        if hasattr(container_class, class_name):
            result_class = getattr(container_class, class_name)
            assert issubclass(result_class, Serializer), "Serializers {} does not inherit from deepomatic.oef.utils.serializer.Serializer".format(package_name + '.' + class_name)
        else:
            result_class = type(class_name, (Serializer,), {})
            setattr(container_class, class_name, result_class)
        return result_class

    return class_helpers.load_proto_class_from_protobuf_descriptor(message,
                                                                   class_type=class_helpers.ClassType.API,
                                                                   getter=get_or_create_serializer)

###############################################################################

class AbstractArrayMapWrapper(object):
    def __init__(self, array_or_map_field, msg, object_fields_to_check, value_serializer_class):
        self._array_or_map_field = array_or_map_field
        self._msg = msg
        self._object_fields_to_check = object_fields_to_check
        self._value_serializer_class = value_serializer_class


class ArrayWrapper(AbstractArrayMapWrapper):
    def add(self, **kwargs):
        container_len = len(self._msg)
        message = self._msg.add(**kwargs)
        set_fields = get_non_none_keys(kwargs)

        # Wrap it into a serializer
        object_key = get_value_key(self._array_or_map_field, container_len)
        assert(object_key not in self._object_fields_to_check)
        serializer = self._value_serializer_class(_msg=message, _set_fields=set_fields)

        # Register it
        self._object_fields_to_check[object_key] = serializer
        return serializer

    def __getitem__(self, key):
        return self._msg[key]

    def __len__(self):
        return len(self._msg)


class MapWrapper(AbstractArrayMapWrapper):
    def __setitem__(self, key, value):
        object_key = get_value_key(self._array_or_map_field, key)
        if object_key in self._object_fields_to_check:
            return self._object_fields_to_check[object_key]
        return self._register(object_key, self._msg[key])

    def __contains__(self, key):
        object_key = get_value_key(self._array_or_map_field, key)
        return object_key in self._object_fields_to_check or key in self._msg

    def __getitem__(self, key):
        object_key = get_value_key(self._array_or_map_field, key)
        if object_key in self._object_fields_to_check:
            return self._object_fields_to_check[object_key]
        else:
            if key in self._msg:
                return self._register(object_key, self._msg[key])
            else:
                raise KeyError(key)

    def __delitem__(self, key):
        object_key = get_value_key(self._array_or_map_field, key)
        del self._object_fields_to_check[object_key]
        del self._msg[key]

    def __len__(self):
        return len(self._msg)

    def _register(self, object_key, message):
        # Wrap it into a serializer
        serializer = self._value_serializer_class(_msg=message)
        # Register it
        self._object_fields_to_check[object_key] = serializer
        return serializer


###############################################################################

class Serializer(object):
    wrapper_class = None
    wrapper_field = None
    optional_fields = []

    def SerializeToBinary(self):
        self._check()
        return self._msg.SerializeToString()

    def SerializeToJson(self):
        self._check()
        return json_format.MessageToJson(self._msg, including_default_value_fields=True, preserving_proto_field_name=True)

    def SerializeToData(self, binary_data=True):
        if binary_data:
            return self.SerializeToBinary()
        else:
            return self.SerializeToJson()

    def ParseFromData(self, data):
        self.loaded_from_external_data = True
        self._msg = parse_protobuf_from_json_or_binary(self.protobuf_class, data)

    def __init__(self, disable_args=None, _msg=None, _set_fields=[], **kwargs):
        """Initialize the protobuf and performs additionnal validation."""
        if disable_args is not None:
            raise SerializerException("You should only initialize serializers with named arguments")

        self.loaded_from_external_data = False
        self._object_fields_to_check = {}

        if _msg is not None:
            if _set_fields is None:
                self._set_fields = set()
                for field in _msg.DESCRIPTOR.fields:
                    if _msg.HasField(field.name):
                        self._set_fields.add(field.name)
            else:
                self._set_fields = set(_set_fields)
            self._msg = _msg
        else:
            kwargs = self._parameter_helper(**kwargs)
            kwargs = self._unbox_parameters(kwargs)
            self._set_fields = get_non_none_keys(kwargs)
            self._set_msg(kwargs)

    ##### private functions

    @classmethod
    def _register(cls, protobuf_module):
        """Sets a wrapper around the protobuf_class to add validation."""
        try:
            cls.protobuf_class = getattr(protobuf_module, cls.__name__)
        except AttributeError:
            # This class does not belong to the protobuf file
            logger.warning("serializer.py: could not find '{}'".format(cls.__name__))
            return
        cls.optional_fields = set(cls.optional_fields)

        # Set object fields
        cls._object_fields = set()
        for f in cls.protobuf_class.DESCRIPTOR.fields:
            if f.message_type is not None:
                cls._object_fields.add(f.name)

        # Set oneofs fields
        oneof_fields = set()
        for oneof in cls.protobuf_class.DESCRIPTOR.oneofs:
            oneof_fields |= set([f.name for f in oneof.fields])

        # Set list and map fields
        msg = cls.protobuf_class()
        list_fields = set()
        map_fields = set()
        for f in cls.protobuf_class.DESCRIPTOR.fields:
            if f.label == FieldDescriptor.LABEL_OPTIONAL and f.name not in cls.optional_fields:
                cls.optional_fields.add(f.name)
            if is_array(msg, f.name):
                list_fields.add(f.name)
            elif is_map(msg, f.name):
                map_fields.add(f.name)

        # Set required fields
        fields = set(cls.protobuf_class.DESCRIPTOR.fields_by_name.keys())
        cls._required_list_fields = (map_fields | list_fields) - oneof_fields - cls.optional_fields
        cls._required_fields      = fields - oneof_fields - cls._required_list_fields - cls.optional_fields

        # Set getter / setter for those fields
        for f in cls.protobuf_class.DESCRIPTOR.fields:
            # Special getter / setter for objects
            if f.name in cls._object_fields and f.message_type.full_name.startswith(module_prefix):
                field_is_map = is_map(msg, f.name)
                field_is_array = is_array(msg, f.name)
                if field_is_map:
                    assert('key' in f.message_type.fields_by_name)
                    assert('value' in f.message_type.fields_by_name)
                    assert(len(f.message_type.fields_by_name) == 2)
                    class_obj = get_or_create_serializer_class_from_protobuf_descriptor(f.message_type.fields_by_name['value'].message_type)
                else:
                    class_obj = get_or_create_serializer_class_from_protobuf_descriptor(f.message_type)

                if class_obj is not None:
                    # Tricky double lambdas to force python to create a closure for each field.
                    # If you don't do that, you end up with all properties pointing to the last field.

                    if field_is_array:
                        getter = (lambda field, class_obj: lambda self: self._get_array_or_map_field(field, class_obj, ArrayWrapper))(f.name, class_obj)
                        setattr(cls, f.name, property(getter))
                        adder = (lambda field, class_obj: lambda self, **kwargs: self._add_object_to_array(field, class_obj, **kwargs))(f.name, class_obj)
                        setattr(cls, 'add_' + f.name, adder)
                        adder_from = (lambda field, class_obj: lambda self, other: self._add_object_to_array_from(field, class_obj, other))(f.name, class_obj)
                        setattr(cls, 'add_' + f.name + '_from', adder_from)
                    elif field_is_map:
                        getter = (lambda field, class_obj: lambda self: self._get_array_or_map_field(field, class_obj, MapWrapper))(f.name, class_obj)
                        setattr(cls, f.name, property(getter))
                        adder = (lambda field, class_obj: lambda self, key: self._add_object_to_map(field, class_obj, key))(f.name, class_obj)
                        setattr(cls, 'add_' + f.name, adder)
                    else:
                        getter = (lambda field, class_obj: lambda self: self._get_object_field(field, class_obj))(f.name, class_obj)
                        setattr(cls, f.name, property(getter))

                    continue

            # Default behaviour: add a property to access the field of the buffer
            # Tricky double lambda to force python to create a closure for each field.
            # If you don't do that, you end up with all properties pointing to the last field.
            getter = (lambda field: lambda self:    self._get_scalar_field(field))(f.name)
            setter = (lambda field: lambda self, x: self._set_scalar_field(field, x))(f.name)
            setattr(cls, f.name, property(getter, setter))

        # Set enum constants
        for (k, enum) in cls.protobuf_class.DESCRIPTOR.enum_values_by_name.items():
            setattr(cls, k, enum.number)

    @staticmethod
    def _parameter_helper(**kwargs):
        """To be overriden for custom input parameters."""
        return kwargs

    @classmethod
    def _unbox_parameters(cls, kwargs):
        """Pass protocol buffers instead of serializers to buffer constructor"""
        kw = {}
        for (field, arg) in kwargs.items():
            if field in cls._object_fields:
                # If we try to construct a list or dict of objects, check them before:
                if isinstance(arg, list):
                    arg = map(lambda obj: obj._msg, arg)
                elif isinstance(arg, dict):
                    arg = dict(map(lambda key_obj: (key_obj[0], key_obj[1]._msg), arg.items()))
                elif isinstance(arg, Serializer):
                    arg = arg._msg
            kw[field] = arg
        return kw

    def _validate(self):
        """To be overriden for custom validation."""
        pass

    def _set_msg(self, kwargs):
        if self.wrapper_class:
            wrapper_args = [kv for kv in kwargs.items() if kv[0] in self.wrapper_class.DESCRIPTOR.fields_by_name]
            for kv in wrapper_args:
                del kwargs[kv[0]]
            wrapper_args.append((self.wrapper_field, self.protobuf_class(**kwargs)))
            self._msg = self.wrapper_class(**dict(wrapper_args))
        else:
            self._msg = self.protobuf_class(**kwargs)

    def _get_msg(self):
        if self.wrapper_class:
            return getattr(self._msg, self.wrapper_field)
        else:
            return self._msg

    def _set_msg_attr(self, field, value):
        if self.wrapper_class:
            msg = getattr(self._msg, self.wrapper_field)
        else:
            msg = self._msg
        setattr(msg, field, value)

    def _get_msg_attr(self, field):
        if self.wrapper_class:
            msg = getattr(self._msg, self.wrapper_field)
        else:
            msg = self._msg
        return getattr(msg, field)

    def _add_object_to_array_base(self, field, serializer_class, other=None, **kwargs):
        # Create a new protobuf message
        message_container = self._get_msg_attr(field)
        container_len = len(message_container)
        message = message_container.add(**kwargs)
        if other is not None:
            set_fields = other._set_fields
            message.CopyFrom(other._get_msg())
        else:
            set_fields = get_non_none_keys(kwargs)

        # Wrap it into a serializer
        object_key = get_value_key(field, container_len)
        assert(object_key not in self._object_fields_to_check)
        serializer = serializer_class(_msg=message, _set_fields=set_fields)

        # Register it
        self._object_fields_to_check[object_key] = serializer
        return serializer

    def _add_object_to_array(self, field, serializer_class, **kwargs):
        # Re-write parameters
        kwargs = serializer_class._parameter_helper(**kwargs)
        kwargs = serializer_class._unbox_parameters(kwargs)
        return self._add_object_to_array_base(field, serializer_class, **kwargs)

    def _add_object_to_array_from(self, field, serializer_class, other):
        return self._add_object_to_array_base(field, serializer_class, other)

    def _add_object_to_map(self, field, serializer_class, key):
        object_key = get_value_key(field, key)
        if object_key in self._object_fields_to_check:
            return self._object_fields_to_check[object_key]

        # Create a new protobuf message
        message = self._get_msg_attr(field)[key]

        # Wrap it into a serializer
        serializer = serializer_class(_msg=message)

        # Register it
        self._object_fields_to_check[object_key] = serializer
        return serializer

    def _get_array_or_map_field(self, field, value_serializer_class, WrapperClass):
        array_or_map = self._get_msg_attr(field)
        return WrapperClass(field, array_or_map, self._object_fields_to_check, value_serializer_class)

    def _get_object_field(self, field, serializer_class):
        f = self._get_msg_attr(field)
        if field not in self._object_fields_to_check:
            self._object_fields_to_check[field] = serializer_class(_msg=f)
        return self._object_fields_to_check[field]

    def _get_scalar_field(self, field):
        return self._get_msg_attr(field)

    def _set_scalar_field(self, field, value):
        self._set_fields.add(field)
        if isinstance(value, Serializer):
            value = value._msg
        self._set_msg_attr(field, value)

    def _check(self):
        if self.loaded_from_external_data:
            # Assuming the buffer was properly serialized
            return

        # Check empty lists
        for f in self._required_list_fields:
            if len(self._get_msg_attr(f)) == 0:
                raise SerializerException("Empty required field: {}".format(f))

        # Check missing fields
        missing_fields = self._required_fields - self._set_fields
        if len(missing_fields) > 0:
            missing_fields = ', '.join(list(missing_fields))
            raise SerializerException("Missing required field(s): {}".format(missing_fields))

        # Check for missing oneofs
        for oneof in self.protobuf_class.DESCRIPTOR.oneofs:
            if self._get_msg().WhichOneof(oneof.name) is None:
                fields = ', '.join([f.name for f in oneof.fields])
                raise SerializerException("Missing one of the field(s): {}".format(fields))

        # Check object fields
        for (field, serializer) in self._object_fields_to_check.items():
            try:
                serializer._check()
            except SerializerException as e:
                raise SerializerException("Field {}: {}".format(field, str(e)))

        self._validate()

def register_all(name, protobuf_module):
    """Register serializer from a module. Pass '__name__' as argument."""
    for message in dir(protobuf_module):
        message = getattr(protobuf_module, message)
        if isinstance(message, GeneratedProtocolMessageType):
            get_or_create_serializer_class_from_protobuf_descriptor(message.DESCRIPTOR)._register(protobuf_module)
