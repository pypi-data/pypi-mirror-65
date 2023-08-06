from ..utils import keep_aspect_ratio_resizer

configs = {
    'Faster RCNN': {
        'meta_arch_default_args': {
            'batch_size': 1,
            'classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            'image_resizer': keep_aspect_ratio_resizer(1024, 1024),
        },
        'backbones_args': {
            'inception_resnet_v2': {'initial_learning_rate': 0.0002},
            'inception_v2': {'initial_learning_rate': 0.0002},
            'nasnet_large': {'initial_learning_rate': 0.0003},
            'pnasnet_large': {'initial_learning_rate': 0.0003},
            'resnet_50_v1': {'initial_learning_rate': 0.0003},
            'resnet_101_v1': {'initial_learning_rate': 0.0003},
            'resnet_152_v1': {'initial_learning_rate': 0.0003},
        },
        'pretrained_weights': {
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
    'RFCN': {
        'meta_arch_default_args': {
            'batch_size': 1,
            'classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            'image_resizer': keep_aspect_ratio_resizer(1024, 1024),
        },
        'backbones_args': {
            'inception_resnet_v2': {'initial_learning_rate': 0.0003},
            'inception_v2': {'initial_learning_rate': 0.0003},
            'nasnet_large': {'initial_learning_rate': 0.0003},
            'pnasnet_large': {'initial_learning_rate': 0.0003},
            'resnet_50_v1': {'initial_learning_rate': 0.0003},
            'resnet_101_v1': {'initial_learning_rate': 0.0003},
            'resnet_152_v1': {'initial_learning_rate': 0.0003},
        },
        'pretrained_weights': {
            'natural_rgb': {
                'resnet_101_v1': 'tensorflow/natural_rgb/resnet_101_v1-rfcn-coco-2018_01_28.tar.gz',
            }
        }
    },
}
