from deepomatic.oef.utils import common
from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import dataset_pb2

class TagAnnotationSpecification(serializer.Serializer):
    """Specification for one source of annotations

    Keyword arguments:
    id -- ID of the tag
    tag_name -- String representing the tag name
    """

class AnnotationSpecification(serializer.Serializer):
    """Specification for one source of annotations

    Keyword arguments:
    tag_spec -- a Tag object
    """

class InputDataSpecification(serializer.Serializer):
    """Specification for one source of input data

    Keyword arguments:
    name -- the annotation name
    type -- the annotation type. Either:
        - InputDataSpecification.IMAGE
    region_annotations -- the list of annotations related to regions
    """
    optional_fields = ['region_annotations']

class Specification(serializer.Serializer):
    """Dataset specifications

    Keyword arguments:
    input_data -- list of input data
    annotations -- list of annotations
    """
    optional_fields = ['annotations']

class SplitByIds(serializer.Serializer):
    """A dataset split where you specify a list of IDs

    Keyword arguments:
    ids -- list of string ids
    """

class Split(serializer.Serializer):
    """A dataset split where you specify the percentage of data involved

    Keyword arguments:
    ids -- list of ids to use for the split.
    """

    def __init__(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = SplitByIds(ids=kwargs['ids'])
        super(Split, self).__init__(**kwargs)

class Splits(serializer.Serializer):
    """Dataset splits

    Keyword arguments:
    split_map -- map of splits identified by name
    reproducible -- If true, SplitByPercentage will lead to the same repartition across runs
    """

class NoRegion(serializer.Serializer):
    """A trivial region representing the whole data"""

class ImageBBox(serializer.Serializer):
    """A 2D bounding box region

    Keyword arguments:
    xmin -- left coordinate
    ymin -- top coordinate
    xmax -- right coordinate
    ymax -- bottom coordinate
    """

    def _validate(self):
        serializer.assert_between_0_and_x(self, 'xmin')
        serializer.assert_between_0_and_x(self, 'ymin')
        serializer.assert_between_0_and_x(self, 'xmax')
        serializer.assert_between_0_and_x(self, 'ymax')

class LabelDistributionEntry(serializer.Serializer):
    """An entry of a probabilistic distribution

    Keyword arguments:
    name / index -- label name or index
    proba -- probability of this label
    """

    def _validate(self):
        serializer.assert_between_0_and_x(self, 'proba')

class LabelDistribution(serializer.Serializer):
    """A probability distribution over labels

    Keyword arguments:
    probas -- a dict of probabilities: {label: value}
    """

    def __init__(self, probas):
        super(LabelDistribution, self).__init__()
        pb = []
        for label, proba in probas.items():
            if isinstance(label, int):
                entry = LabelDistributionEntry(index=label, proba=proba)
            else:
                entry = LabelDistributionEntry(name=label, proba=proba)
            pb.append(entry.msg())
        self.probas.extend(pb)

class Annotation(serializer.Serializer):
    """An annotation

    Keyword arguments:
    name -- annotation name (see specifications)
    value -- a value
    """

    @staticmethod
    def _parameter_helper(name, value):
        if isinstance(value, bool):
            key = 'bool_value'
        elif common.is_string(value):
            key = 'string_value'
        elif isinstance(value, int):
            key = 'int_value'
        elif isinstance(value, float):
            key = 'float_value'
        elif isinstance(value, LabelDistribution):
            key = 'distribution_value'
        else:
            raise Exception("Unexpected value type.")
        return {'name': name, key: value}

class Region(serializer.Serializer):
    """An data region

    Keyword arguments:
    annotations -- annotation array
    region -- the region
    """
    optional_fields = ['annotations']

    @staticmethod
    def _parameter_helper(region=None, annotations=[]):
        if region is None:
            region = NoRegion()  # cannot be used as a default argument as the class is not registred yet
        if isinstance(region, NoRegion):
            key = 'none'
            region_type = Region.NONE
        elif isinstance(region, ImageBBox):
            key = 'image_bbox'
            region_type = Region.IMAGE_BBOX
        else:
            raise Exception("Unexpected region type: {}".format(str(region.__class__)))
        return {'type': region_type, 'annotations': annotations, key: region}

class InputData(serializer.Serializer):
    """An input data

    Keyword arguments:
    name -- input data name
    value / value_from -- the value / a file containing the value
    regions -- array of regions
    """
    optional_fields = ['regions']

class DataPoint(serializer.Serializer):
    """A data point with its input data and annotations

    Keyword arguments:
    id -- input data ID
    input_data -- array of input data
    annotations -- array of annotations
    meta -- free style user specific JSON field
    """
    optional_fields = ['annotations', 'meta']

class DatasetConfig(serializer.Serializer):
    """Full dataset configuration object

    Keyword arguments:
    specification -- a Specification field
    splits -- a dictionnary with split names as keys and list of IDs as values, e.g.:
        {
            "train": ["1", "2"],
            "val":   ["3", "4"]
        }
    data_points -- an array of data points
    """
    #TODO: of a oneof + map splits: to allow various configs

class Dataset(serializer.Serializer):
    optional_fields = ['operations']

    def __init__(self, config=None, config_path=None, *args, **kwargs):
        if config is not None and config_path is not None:
            raise serializer.SerializerException("You cannot specify both 'config' and 'config_path'")
        super(Dataset, self).__init__(config=config, config_path=config_path, *args, **kwargs)

serializer.register_all(__name__, dataset_pb2)
