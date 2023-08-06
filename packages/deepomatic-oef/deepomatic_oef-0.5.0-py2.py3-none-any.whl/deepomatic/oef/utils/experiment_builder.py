from google.protobuf.descriptor import FieldDescriptor

from deepomatic.oef.configs import model_list
from deepomatic.oef.utils import class_helpers
from deepomatic.oef.utils.serializer import Serializer
from deepomatic.oef.protos.experiment_pb2 import Experiment
from deepomatic.oef.experiment import Experiment as ExperimentWrapper
import logging

logger = logging.getLogger(__name__)


class InvalidNet(Exception):
    pass


class ExperimentBuilder(object):
    """
    This class can build a Experiment protobuf given the pre-determined parameters. You can also pass
    additionnal parameters to override the default arguments. In that purpose, all fields of Model and its
    sub-messages are assumed to have a different name (this assumpition is checked by model_generator).
    """

    _model_list = None

    def __init__(self, model_type_key):
        if self._model_list is None:
            self.load_model_list()
        if model_type_key not in self._model_list:
            # Try model_type_key reordering to provide backward compatibility with oef<0.5.0
            model_type_key_parts = model_type_key.split('.')
            model_type_key_orig = model_type_key
            model_type_key = '.'.join([model_type_key_parts[0], model_type_key_parts[-1]] + model_type_key_parts[1:-1])
            logger.warning("Model not found: '{}', trying with '{}'".format(model_type_key_orig, model_type_key))
            if model_type_key not in self._model_list:
                raise InvalidNet("Unknown model {}".format(model_type_key))
        self._model_args = self._model_list[model_type_key]

    def get_model_param(self, param):
        """
        Search in args and default_args for `param`. This permits searching for a default parameter
        from the model_list, after an Experiment has been built.
        Warning: this should be used as a last resort, when you need a param from an Experiment, before even building it.
        ```
        builder = ExperimentBuilder(...)
        batch_size = builder.get_model_param('batch_size')
        xp = builder.build(num_train_steps = n / batch_size)
        ```
        All protobuf default params are exposed once it's built.
        """
        if param in self._model_args.default_args:
            return self._model_args.default_args[param]
        else:
            logger.warn('Parameter not found in experiment builder: {}. Available model args are: {}'.format(param, self._model_args))

    @classmethod
    def load_model_list(cls):
        # Avoid to load it at the root of the module to avoid nested import loops
        cls._model_list = {}
        for key, args in model_list.model_list.items():
            assert key not in cls._model_list, "Duplicate model key, this should not happen"
            cls._model_list[key] = args

    def build(self, **kwargs):
        all_args = set()
        all_args.update(self._model_args.default_args.keys())
        all_args.update(kwargs.keys())
        used_args = set()
        xp = self._recursive_build_(Experiment, self._model_args.default_args, kwargs, used_args)
        unused_args = all_args - used_args
        if len(unused_args) > 0:
            raise Exception('Unused keyword argument: {}'.format(', '.join(unused_args)))
        return ExperimentWrapper(_msg=xp, _set_fields=None)

    @staticmethod
    def _recursive_build_(protobuf_class, default_args, kwargs, used_args):
        real_args = {}
        for field in protobuf_class.DESCRIPTOR.fields:
            if field.name in kwargs:
                used_args.add(field.name)
                value = kwargs[field.name]
                if isinstance(value, Serializer):
                    value = value._msg
                real_args[field.name] = value
            elif field.name in default_args:
                used_args.add(field.name)
                real_args[field.name] = default_args[field.name]
            elif field.message_type is not None:
                if field.label == FieldDescriptor.LABEL_REQUIRED:  # we build the message if it is required
                    # This fields is a protobuf message, we build it recursively
                    real_args[field.name] = ExperimentBuilder._recursive_build_(class_helpers.load_proto_class_from_protobuf_descriptor(field.message_type), default_args, kwargs, used_args)

        return protobuf_class(**real_args)
