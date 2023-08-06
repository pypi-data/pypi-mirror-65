from ..utils import fixed_shape_resizer

configs = {
    'AttentionOCR': {
        'meta_arch_default_args': {
            'batch_size': 32,
            'classification_loss': {'weighted_softmax': {'logit_scale': 1.0}},
            'data_augmentation_options': [],
            'image_resizer': fixed_shape_resizer(102, 32),
        },
        'backbones_args': {
            'inception_v3': {'initial_learning_rate': 0.004},
        },
        'pretrained_weights': {
            'natural_rgb': {
                'inception_v3': 'tensorflow/natural_rgb/inception_v3-classification-imagenet2012-2016_08_28.ckpt',
            }
        }
    },
}
