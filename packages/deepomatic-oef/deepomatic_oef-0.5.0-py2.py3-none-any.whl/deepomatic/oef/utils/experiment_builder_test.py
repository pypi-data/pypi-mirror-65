import pytest

import deepomatic.oef.dataset as dataset
from deepomatic.oef.utils.experiment_builder import ExperimentBuilder, InvalidNet
from deepomatic.oef.configs import model_list


def test_new_model_key():
    # Try should not raise an exception
    ExperimentBuilder("image_detection.pretraining_natural_rgb.faster_rcnn.resnet_50_v1")

def test_old_model_key():
    # Try should not raise an exception
    ExperimentBuilder("image_detection.faster_rcnn.resnet_50_v1.pretraining_natural_rgb")

def test_bad_model_key():
    with pytest.raises(InvalidNet):
        ExperimentBuilder("image_detection.foo.resnet_50_v1.pretraining_natural_rgb")

def test_builder():
    # Tests mini pets dataset with 3 classes
    ds = dataset.Dataset(root='gs://my/bucket', config_path='config.prototxt')
    for key in model_list.model_list:
        builder = ExperimentBuilder(key)
        xp = builder.build(dataset=ds, exclusive_labels=True)
        xp.SerializeToBinary()
