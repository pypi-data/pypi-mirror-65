import tempfile
import importlib.util

from .model_list_generator import generate


def test_generate():
    _, tmp_file = tempfile.mkstemp(suffix='.py')
    # We check no exception is raised
    generate(tmp_file)

    # We try to load the generated module
    spec = importlib.util.spec_from_file_location("module.name", tmp_file)
    model_list_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_list_module)

    # We do simple checks to verify the model list has the expected structure
    assert "image_detection.pretraining_natural_rgb.faster_rcnn.resnet_50_v1" in model_list_module.model_list
    for key, model_args in model_list_module.model_list.items():
        if not key.endswith('pretraining_none'):
            assert('pretrained_parameters' in model_args.default_args, "Missing pretrained parameters in: '{}'".format(key))
