from ..utils import fixed_shape_resizer

configs = {
    'SSD': {
        'meta_arch_default_args': {
            'batch_size': 24,
            'classification_loss': {'weighted_sigmoid': {}},
            'image_resizer': fixed_shape_resizer(300, 300),
        },
        'backbones_args': {
            'inception_v2': {'initial_learning_rate': 0.004},
            'inception_v3': {'initial_learning_rate': 0.004},
            'mobilenet_v1': {'initial_learning_rate': 0.004},
            'mobilenet_v2': {'initial_learning_rate': 0.004},
            'resnet_50_v1': {
                'initial_learning_rate': 0.004,
                # 'classification_loss': {'weighted_sigmoid_focal': {'gamma': 2, 'alpha': 0.25}}
            },
            'resnet_101_v1': {
                'initial_learning_rate': 0.004,
                # 'classification_loss': {'weighted_sigmoid_focal': {'gamma': 2, 'alpha': 0.25}}
            },
            'resnet_152_v1': {
                'initial_learning_rate': 0.004,
                # 'classification_loss': {'weighted_sigmoid_focal': {'gamma': 2, 'alpha': 0.25}}
            },
        },
        'pretrained_weights': {
            'natural_rgb': {
                'inception_v2': 'tensorflow/natural_rgb/inception_v2-ssd-coco-2018_01_28.tar.gz',
                'mobilenet_v1': 'tensorflow/natural_rgb/mobilenet_v1-ssd-coco-2018_01_28.tar.gz',
                'mobilenet_v2': 'tensorflow/natural_rgb/mobilenet_v2-ssd-coco-2018_03_29.tar.gz',
                # See: https://github.com/Deepomatic/thoth/issues/277
                # 'resnet_50_v1': 'tensorflow/natural_rgb/resnet_50_v1_fpn-ssd-coco-2018_07_03.tar.gz',
            }
        }
    },
    'SSD Lite': {
        'meta_arch_default_args': {
            'batch_size': 24,
            'classification_loss': {'weighted_sigmoid': {}},
            'image_resizer': fixed_shape_resizer(300, 300),
        },
        'backbones_args': {
            'inception_v2': {'initial_learning_rate': 0.004, 'override_base_feature_extractor_hyperparams': True},
            'inception_v3': {'initial_learning_rate': 0.004, 'override_base_feature_extractor_hyperparams': True},
            'mobilenet_v1': {'initial_learning_rate': 0.004},
            'mobilenet_v2': {'initial_learning_rate': 0.004},
            'resnet_50_v1': {'initial_learning_rate': 0.004},
            'resnet_101_v1': {'initial_learning_rate': 0.004},
            'resnet_152_v1': {'initial_learning_rate': 0.004},
        },
        'pretrained_weights': {
            'natural_rgb': {
                'mobilenet_v2': 'tensorflow/natural_rgb/mobilenet_v2-ssd_lite-coco-2018_05_09.tar.gz',
            }
        }
    },
}
