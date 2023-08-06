from ..utils import fixed_shape_resizer

configs = {
    'YOLO v2': {
        'meta_arch_default_args': {
            'batch_size': 64,
            'classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            'image_resizer': fixed_shape_resizer(416, 416),
        },
        'backbones_args': {
            'darknet_19': {'initial_learning_rate': 0.01, 'data_augmentation_options': []},
        },
        'pretrained_weights': {
            'natural_rgb': {
                'darknet_19': 'darknet/natural_rgb/darknet19-yolo-voc2007.weights',
            }
        }
    },
    'YOLO v3': {
        'meta_arch_default_args': {
            'batch_size': 64,
            'classification_loss': {'weighted_sigmoid': {}},
            'image_resizer': fixed_shape_resizer(416, 416),
        },
        'backbones_args': {
            'darknet_53': {'initial_learning_rate': 0.01, 'data_augmentation_options': []},
        },
        'pretrained_weights': {
            'natural_rgb': {
                'darknet_53': 'darknet/natural_rgb/darknet53-yolo-imagenet2012.weights',
            }
        }
    },
}
