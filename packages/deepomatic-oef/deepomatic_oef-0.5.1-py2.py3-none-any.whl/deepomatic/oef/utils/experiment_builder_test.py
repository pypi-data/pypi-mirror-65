import pytest

import deepomatic.oef.dataset as dataset
from deepomatic.oef.utils.experiment_builder import ExperimentBuilder, InvalidNet
from deepomatic.oef.configs import model_list


FAKE_DATASET = dataset.Dataset(root='gs://my/bucket', config_path='config.prototxt')


def test_new_model_key():
    # Try should not raise an exception
    ExperimentBuilder("image_detection.pretraining_natural_rgb.faster_rcnn.resnet_50_v1")

def test_old_model_key():
    # Try should not raise an exception
    ExperimentBuilder("image_detection.faster_rcnn.resnet_50_v1.pretraining_natural_rgb")

def test_bad_model_key():
    with pytest.raises(InvalidNet):
        ExperimentBuilder("image_detection.foo.resnet_50_v1.pretraining_natural_rgb")


# Do not rename this test: it is used in the Mafile in `make models`
@pytest.mark.parametrize(
    'model_key', list(model_list.model_list.keys())
)
def test_builder(model_key):
    # Tests mini pets dataset with 3 classes
    builder = ExperimentBuilder(model_key)
    xp = builder.build(dataset=FAKE_DATASET, exclusive_labels=True)
    xp.SerializeToBinary()
