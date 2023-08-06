from abc import ABC, abstractmethod

from enum import Enum


# -----------------------------------------------------------------------------#

class ModelInterface(ABC):
    """
    This is the base class for any specific model implementation that is part of
    the `model` OneOf field of ../protos/model.proto
    """

    class BackendType(Enum):
        TENSORFLOW = 'tensorflow'
        DARKNET = 'darknet'

    @classmethod
    @abstractmethod
    def get_backend(cls, model_type):
        """
        Return the back-end that should be used.

        Args:
            model_type: a ModelType protobuf

        Return:
            - An instance of BackendType.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_metrics():
        """Should return a list of thoth.core.evaluation.metrics.MetricBuilder objects"""
        pass

    @abstractmethod
    def get_vulcan_preprocessing(self):
        """Should be implemented by back-end classes to return the dict to send to Vulcan"""
        pass

    @abstractmethod
    def get_vulcan_recognition_spec(self, global_vars):
        """
        Return vulcan the ouptut JSON data needed to create a recognition spec. Overriden for OCR models.
        """
        pass

    @abstractmethod
    def get_vulcan_postprocessing_for_network(self, global_vars):
        """Should be implemented by back-end classes to return the dict to send to Vulcan"""
        pass

    @abstractmethod
    def get_vulcan_postprocessing_for_recognition(self, global_vars):
        """Should be implemented by back-end classes to return the dict to send to Vulcan"""
        pass

    @abstractmethod
    def get_network_metadata(self, global_vars):
        """Should be implemented by back-end classes to return the dict of metadata to attach to a network"""
        pass


# -----------------------------------------------------------------------------#

class TensorflowModelInterface(ModelInterface):

    @abstractmethod
    def get_max_number_of_proposals(self):
        """
        This is a big hack for now.
        We depend on tensorflow/models for the groundtruth tensors elaboration.
        The groundtruth_classes tensors is of size [batch_size, max_number_of_boxes, num_classes]
        For detection we need to put max_number_of_boxes == 100
        For classification we need to put max_number_of_boxes == 1 and then squeeze the tensor
        """
        pass

    @abstractmethod
    def get_model_fn(self, mode):
        """
        Return a function that will be applied to preprocessed inputs.

        Args:
            mode: tf.estimator.ModeKeys.TRAIN or tf.estimator.ModeKeys.TEST

        Return
        """
        pass

    @abstractmethod
    def get_groundtruth(self, mode, annotations):
        """
        Returns groundtruth tensors.

        Args:
            mode (tf.estimator.ModeKeys): tf.estimator.ModeKeys.TRAIN / EVAL / PREDICT
            annotations (dict of tensors): the annotation dict tensor

        Return:
            A groundtruth object that will be passed to `get_prediction_dict`, `get_loss_dict` and `get_eval_metrics`.
        """
        pass

    @abstractmethod
    def get_preprocess_fn(self):
        """
        Returns the function to apply to the input tensor for this model. The input has already been "data augmented" so you
        typically want to resize and centrate it.

        Returns:
            The preprocessing function must return the preprocessed input and its original shape.
        """
        pass

    @abstractmethod
    def get_predictions(self, mode, model, input_data, groundtruth=None):
        """
        Returns raw predictions (typically logits).

        Args:
            mode (tf.estimator.ModeKeys): tf.estimator.ModeKeys.TRAIN / EVAL / PREDICT
            model (object): the model as returned by `model_fn`
            input_data (dict of tensors): the dictionary of input tensors
            groundtruth (object): the groundtruth object as returned by `get_groundtruth`

        Returns:
            A predictions object that will be passed to `postprocess_predictions` and `get_eval_metrics`
        """
        pass

    @abstractmethod
    def postprocess_predictions(self, model, input_data, predictions):
        """
        Apply a final post-processing step to predictions.

        Args:
            model (object): the model as returned by `model_fn`
            input_data (dict of tensors): the dictionary of input tensors
            predictions (object): the predictions object as returned by `get_predictions`

        Returns:
            A dictionary of tensors with keys being the same as the dict returned by
            `get_export_tensors_fn_dict`
        """
        pass

    @abstractmethod
    def get_restore_map(self, model, checkpoint_path):
        """
        Returns available variables from checkpoint.

        Args:
            model (object): the model as returned by `model_fn`
            checkpoint_path (string): path to checkpoint file

        Returns:
            An `assignment_map` as used by tf.train.init_from_checkpoint.
            Cf https://www.tensorflow.org/api_docs/python/tf/train/init_from_checkpoint
        """
        pass

    @abstractmethod
    def get_loss_dict(self, mode, model, input_data, predictions, groundtruth):
        """
        Returns a dictionary of losses

        Args:
            mode (tf.estimator.ModeKeys): tf.estimator.ModeKeys.TRAIN / EVAL / PREDICT
            model (object): the model as returned by `model_fn`
            input_data (dict of tensors): the dictionary of input tensors
            predictions (object): the predictions object as returned by `get_predictions`
            groundtruth (object): the groundtruth object as returned by `get_groundtruth`

        Returns:
            A dictionary of losses.
        """
        pass

    @abstractmethod
    def get_regularization_losses(self, model):
        """
        Returns a list of regularization losses
        """
        pass

    @abstractmethod
    def get_update_ops(self, model):
        """
        Returns tensorflow update ops
        """
        pass

    @abstractmethod
    def get_eval_metrics(self, model, input_data, postprocessed_predictions, groundtruth):
        """
        Returns a dictionary of metrics

        Args:
            model (object): the model as returned by `model_fn`
            input_data (dict of tensors): the dictionary of input tensors
            postprocessed_predictions (dict of tensors): the post-processed predictions object as returned by `postprocess_predictions`
            groundtruth (object): the groundtruth object as returned by `get_groundtruth`

        Returns:
            A dictionary of metrics.
        """
        pass

    @abstractmethod
    def get_export_tensors_fn_dict(self):
        """
        Returns a dictionary of function (the values) to apply of post-processed prediction tensors
        (the keys, which must match keys from `postprocess_predictions` output)
        """
        pass

# -----------------------------------------------------------------------------#

class MetaArchInterface(ABC):
    """
    This is the base class for any specific model implementation that is part of
    the `meta_arch` OneOf field of a model.
    """
