from ..utils import fixed_shape_resizer

configs = {
    'yolo_v2': {
        'display_name': 'YOLO v2',
        'model_default_args': {
            'batch_size': 64,
            '@model.classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            '@model.image_resizer': fixed_shape_resizer(416, 416),
            '@model.data_augmentation_options': [],
        },
        'model_meta_arch': 'yolo_v2',
        'backbones': {
            'darknet_19': {'initial_learning_rate': 0.01},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                'darknet_19': 'darknet/natural_rgb/darknet19-yolo-voc2007.weights',
            }
        }
    },
    'yolo_v3': {
        'display_name': 'YOLO v3',
        'model_default_args': {
            'batch_size': 64,
            '@model.classification_loss': {'weighted_sigmoid': {}},
            '@model.image_resizer': fixed_shape_resizer(416, 416),
            '@model.data_augmentation_options': [],
        },
        'model_meta_arch': 'yolo_v3',
        'backbones': {
            'darknet_53': {'initial_learning_rate': 0.01},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                'darknet_53': 'darknet/natural_rgb/darknet53-yolo-imagenet2012.weights',
            }
        }
    },
}
