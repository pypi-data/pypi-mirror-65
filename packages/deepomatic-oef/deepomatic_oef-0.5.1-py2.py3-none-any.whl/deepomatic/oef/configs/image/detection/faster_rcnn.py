from ..utils import keep_aspect_ratio_resizer

configs = {
    'faster_rcnn': {
        'display_name': 'Faster RCNN',
        'model_default_args': {
            'batch_size': 1,
            '@model.classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            '@model.image_resizer': keep_aspect_ratio_resizer(1024, 1024),
            '@model.data_augmentation_options': [{'random_horizontal_flip': {'keypoint_flip_permutation': []}}],
        },
        'model_meta_arch': 'faster_rcnn',
        'backbones': {
            'inception_resnet_v2': {'initial_learning_rate': 0.0002},
            'inception_v2': {'initial_learning_rate': 0.0002},
            'nasnet_large': {'initial_learning_rate': 0.0003},
            'pnasnet_large': {'initial_learning_rate': 0.0003},
            'resnet_50_v1': {'initial_learning_rate': 0.0003},
            'resnet_101_v1': {'initial_learning_rate': 0.0003},
            'resnet_152_v1': {'initial_learning_rate': 0.0003},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                # See: https://github.com/Deepomatic/thoth/issues/230
                # 'inception_resnet_v2': 'tensorflow/natural_rgb/inception_resnet_v2-faster_rcnn-coco-2018_01_28.tar.gz',
                # See: https://github.com/Deepomatic/thoth/issues/276
                # 'nasnet_large': 'tensorflow/natural_rgb/nasnet_large-faster_rcnn-coco-2018_01_28.tar.gz',
                'resnet_50_v1': 'tensorflow/natural_rgb/resnet_50_v1-faster_rcnn-coco-2018_01_28.tar.gz',
                'resnet_101_v1': 'tensorflow/natural_rgb/resnet_101_v1-faster_rcnn-coco-2018_01_28.tar.gz',
            }
        }
    },
    'rfcn': {
        'display_name': 'RFCN',
        'model_default_args': {
            'batch_size': 1,
            '@model.classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            '@model.image_resizer': keep_aspect_ratio_resizer(1024, 1024),
            '@model.data_augmentation_options': [{'random_horizontal_flip': {'keypoint_flip_permutation': []}}],
        },
        'model_meta_arch': 'rfcn',
        'backbones': {
            'inception_resnet_v2': {'initial_learning_rate': 0.0003},
            'inception_v2': {'initial_learning_rate': 0.0003},
            'nasnet_large': {'initial_learning_rate': 0.0003},
            'pnasnet_large': {'initial_learning_rate': 0.0003},
            'resnet_50_v1': {'initial_learning_rate': 0.0003},
            'resnet_101_v1': {'initial_learning_rate': 0.0003},
            'resnet_152_v1': {'initial_learning_rate': 0.0003},
        },
        'pretrained_parameters': {
            'natural_rgb': {
                'resnet_101_v1': 'tensorflow/natural_rgb/resnet_101_v1-rfcn-coco-2018_01_28.tar.gz',
            }
        }
    },
}
