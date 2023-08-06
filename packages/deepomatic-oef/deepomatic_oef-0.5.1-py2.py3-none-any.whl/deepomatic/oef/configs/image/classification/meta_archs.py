from ...utils import dict_inject
from ..utils import fixed_shape_resizer

common_config = {
    'model_default_args': {
        '@model.backbone.data_augmentation_options': [{'random_horizontal_flip': {'keypoint_flip_permutation': []}}],
    },
    'model_meta_arch': None,
    'backbones': {
        'vgg_11': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.5}},
        'vgg_16': {'batch_size': 32, 'initial_learning_rate': 0.005, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.5}},
        'vgg_19': {'batch_size': 32, 'initial_learning_rate': 0.0025, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.5}},
        'inception_v1': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.8}},
        'inception_v2': {'batch_size': 32, 'initial_learning_rate': 0.0025, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.8}},
        'inception_v3': {'batch_size': 32, 'initial_learning_rate': 0.005, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(299, 299)}, 'dropout_keep_prob': 0.8}},
        'inception_v4': {'batch_size': 32, 'initial_learning_rate': 0.005, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(299, 299)}, 'dropout_keep_prob': 0.8}},
        'inception_resnet_v2': {'batch_size': 32, 'initial_learning_rate': 0.005, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(299, 299)}, 'dropout_keep_prob': 0.8}},
        'resnet_50_v1': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},  # TODO: try with dropout ?
        'resnet_101_v1': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'resnet_152_v1': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'resnet_200_v1': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'resnet_50_v2': {'batch_size': 32, 'initial_learning_rate': 0.025, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'resnet_101_v2': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'resnet_152_v2': {'batch_size': 32, 'initial_learning_rate': 0.0025, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'resnet_200_v2': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'mobilenet_v1': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.999}},
        'mobilenet_v1_075': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.999}},
        'mobilenet_v1_050': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.999}},
        'mobilenet_v1_025': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.999}},
        'mobilenet_v2': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},  # TODO: try with dropout ?
        'mobilenet_v2_140': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
        'nasnet_mobile': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.5}},
        'nasnet_large': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(331, 331)}, 'dropout_keep_prob': 0.5}},
        'pnasnet_large': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(331, 331)}, 'dropout_keep_prob': 0.5}},
        'pnasnet_mobile': {'batch_size': 32, 'initial_learning_rate': 0.01, '@model': {'backbone': {'image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 0.5}},
        'efficientnet_b0': {'batch_size': 32, 'initial_learning_rate': 0.004, '@model': {'backbone': {'width_multiplier': 1.0, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 224, 'width': 224, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.8}},
        'efficientnet_b1': {'batch_size': 32, 'initial_learning_rate': 0.004, '@model': {'backbone': {'width_multiplier': 1.0, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 240, 'width': 240, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.8}},
        'efficientnet_b2': {'batch_size': 32, 'initial_learning_rate': 0.004, '@model': {'backbone': {'width_multiplier': 1.1, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 260, 'width': 260, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.7}},
        'efficientnet_b3': {'batch_size': 32, 'initial_learning_rate': 0.004, '@model': {'backbone': {'width_multiplier': 1.2, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 300, 'width': 300, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.7}},
        'efficientnet_b4': {'batch_size': 16, 'initial_learning_rate': 0.002, '@model': {'backbone': {'width_multiplier': 1.4, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 380, 'width': 380, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.6}},
        'efficientnet_b5': {'batch_size': 8, 'initial_learning_rate': 0.001, '@model': {'backbone': {'width_multiplier': 1.6, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 456, 'width': 456, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.6}},
        'efficientnet_b6': {'batch_size': 4, 'initial_learning_rate': 0.0005, '@model': {'backbone': {'width_multiplier': 1.8, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 528, 'width': 528, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.5}},
        'efficientnet_b7': {'batch_size': 2, 'initial_learning_rate': 0.00025, '@model': {'backbone': {'width_multiplier': 2.0, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 600, 'width': 600, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.5}},
        'efficientnet_b8': {'batch_size': 1, 'initial_learning_rate': 0.000125, '@model': {'backbone': {'width_multiplier': 2.2, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 672, 'width': 672, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.5}},
        'efficientnet_l2': {'batch_size': 1, 'initial_learning_rate': 0.000125, '@model': {'backbone': {'width_multiplier': 4.3, 'min_width': 8, 'image_resizer': {'fixed_shape_resizer': {'height': 800, 'width': 800, 'resize_method': 'BICUBIC'}}}, 'dropout_keep_prob': 0.5}},
    },
    'pretrained_parameters': {
        'natural_rgb': {  # Use 'None' to refer to the default back-bone weights
            'vgg_16': None,
            'vgg_19': None,
            'inception_v1': None,
            'inception_v2': None,
            'inception_v3': None,
            'inception_v4': None,
            'inception_resnet_v2': None,
            'resnet_50_v1': None,
            'resnet_101_v1': None,
            'resnet_152_v1': None,
            'resnet_50_v2': None,
            'resnet_101_v2': None,
            'resnet_152_v2': None,
            'mobilenet_v1': None,
            'mobilenet_v1_050': None,
            'mobilenet_v1_025': None,
            'mobilenet_v2': None,
            'mobilenet_v2_140': None,
            'nasnet_mobile': None,
            'nasnet_large': None,
            'pnasnet_large': None,
            'pnasnet_mobile': None,
            'efficientnet_b0': None,
            'efficientnet_b1': None,
            'efficientnet_b2': None,
            'efficientnet_b3': None,
            'efficientnet_b4': None,
            'efficientnet_b5': None,
            'efficientnet_b6': None,
            'efficientnet_b7': None,
            'efficientnet_b8': None,
            'efficientnet_l2': None,
        }
    }
}


configs = {
    'softmax': dict_inject(common_config, {
        'display_name': 'Softmax',
        'model_default_args': {
            '@model.loss': {'weighted_softmax': {'logit_scale': 1.0}},
        }
    }),
    'sigmoid': dict_inject(common_config, {
        'display_name': 'Sigmoid',
        'model_default_args': {
            '@model.loss': {'weighted_sigmoid': {}},
        }
    }),
}
