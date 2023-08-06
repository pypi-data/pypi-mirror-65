backbones = {
    'vgg_11': {
        'display_name': 'VGG 11',
        'backbone_args': {'vgg': {'depth': 11}},
    },
    'vgg_16': {
        'display_name': 'VGG 16',
        'backbone_args': {'vgg': {'depth': 16}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/vgg_16-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'vgg_19': {
        'display_name': 'VGG 19',
        'backbone_args': {'vgg': {'depth': 19}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/vgg_19-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'inception_v1': {
        'display_name': 'Inception v1',
        'backbone_args': {'inception': {'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'inception_v2': {
        'display_name': 'Inception v2',
        'backbone_args': {'inception': {'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v2-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'inception_v3': {
        'display_name': 'Inception v3',
        'backbone_args': {'inception': {'version': 3}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v3-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'inception_v4': {
        'display_name': 'Inception v4',
        'backbone_args': {'inception': {'version': 4}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v4-classification-imagenet2012-2016_09_09.ckpt'
        },
    },
    'inception_resnet_v2': {
        'display_name': 'Inception ResNet v2',
        'backbone_args': {'inception_resnet': {'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_resnet_v2-classification-imagenet2012-2016_08_30.ckpt'
        },
    },
    'resnet_50_v1': {
        'display_name': 'ResNet 50 v1',
        'backbone_args': {'resnet': {'depth': 50, 'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_50_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'resnet_101_v1': {
        'display_name': 'ResNet 101 v1',
        'backbone_args': {'resnet': {'depth': 101, 'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_101_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'resnet_152_v1': {
        'display_name': 'ResNet 152 v1',
        'backbone_args': {'resnet': {'depth': 152, 'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_152_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    'resnet_200_v1': {
        'display_name': 'ResNet 200 v1',
        'backbone_args': {'resnet': {'depth': 200, 'version': 1}},
    },
    'resnet_50_v2': {
        'display_name': 'ResNet 50 v2',
        'backbone_args': {'resnet': {'depth': 50, 'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_50_v2-classification-imagenet2012-2017_04_14.ckpt'
        },
    },
    'resnet_101_v2': {
        'display_name': 'ResNet 101 v2',
        'backbone_args': {'resnet': {'depth': 101, 'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_101_v2-classification-imagenet2012-2017_04_14.ckpt'
        },
    },
    'resnet_152_v2': {
        'display_name': 'ResNet 152 v2',
        'backbone_args': {'resnet': {'depth': 152, 'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_152_v2-classification-imagenet2012-2017_04_14.ckpt'
        },
    },
    'resnet_200_v2': {
        'display_name': 'ResNet 200 v2',
        'backbone_args': {'resnet': {'depth': 200, 'version': 2}},
    },
    'mobilenet_v1': {
        'display_name': 'MobileNet v1',
        'backbone_args': {'mobilenet': {'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v1-classification-imagenet2012-2018_02_22.tar.gz'
        },
    },
    'mobilenet_v1_075': {
        'display_name': 'MobileNet v1 75%',
        'backbone_args': {'mobilenet': {'version': 1}, 'width_multiplier': 0.75},
    },
    'mobilenet_v1_050': {
        'display_name': 'MobileNet v1 50%',
        'backbone_args': {'mobilenet': {'version': 1}, 'width_multiplier': 0.50},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v1_050-classification-imagenet2012-2018_02_22.tar.gz'
        },
    },
    'mobilenet_v1_025': {
        'display_name': 'MobileNet v1 25%',
        'backbone_args': {'mobilenet': {'version': 1}, 'width_multiplier': 0.25},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v1_025-classification-imagenet2012-2018_02_22.tar.gz'
        },
    },
    'mobilenet_v2': {
        'display_name': 'MobileNet v2',
        'backbone_args': {'mobilenet': {'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v2-classification-imagenet2012-2018_03_28.tar.gz'
        },
    },
    'mobilenet_v2_140': {
        'display_name': 'MobileNet v2 140%',
        'backbone_args': {'mobilenet': {'version': 2}, 'width_multiplier': 1.4},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v2_140-classification-imagenet2012-2018_03_28.tar.gz'
        },
    },
    'nasnet_large': {
        'display_name': 'NasNet Large',
        'backbone_args': {'nasnet': {'depth': 0, 'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/nasnet_large-classification-imagenet2012-2017_10_04.tar.gz'
        },
    },
    'nasnet_mobile': {
        'display_name': 'NasNet Mobile',
        'backbone_args': {'nasnet': {'depth': 1, 'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/nasnet_mobile-classification-imagenet2012-2017_10_04.tar.gz'
        },
    },
    'pnasnet_large': {
        'display_name': 'PNasNet Large',
        'backbone_args': {'nasnet': {'depth': 0, 'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/pnasnet_large-classification-imagenet2012-2017_12_13.tar.gz'
        },
    },
    'pnasnet_mobile': {
        'display_name': 'PNasNet Mobile',
        'backbone_args': {'nasnet': {'depth': 1, 'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/pnasnet_mobile-classification-imagenet2012-2017_12_13.tar.gz'
        },
    },
    'darknet_19': {
        'display_name': 'Darknet 19',
        'backbone_args': {'darknet': {'depth': 19}},
        'pretrained_parameters': {
        },
    },
    'darknet_53': {
        'display_name': 'Darknet 53',
        'backbone_args': {'darknet': {'depth': 53}},
        'pretrained_parameters': {
        },
    },
    'efficientnet_b0': {
        'display_name': 'EfficientNet-B0',
        'backbone_args': {'efficientnet': {'version': 0}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b0_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b1': {
        'display_name': 'EfficientNet-B1',
        'backbone_args': {'efficientnet': {'version': 1}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b1_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b2': {
        'display_name': 'EfficientNet-B2',
        'backbone_args': {'efficientnet': {'version': 2}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b2_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b3': {
        'display_name': 'EfficientNet-B3',
        'backbone_args': {'efficientnet': {'version': 3}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b3_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b4': {
        'display_name': 'EfficientNet-B4',
        'backbone_args': {'efficientnet': {'version': 4}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b4_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b5': {
        'display_name': 'EfficientNet-B5',
        'backbone_args': {'efficientnet': {'version': 5}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b5_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b6': {
        'display_name': 'EfficientNet-B6',
        'backbone_args': {'efficientnet': {'version': 6}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b6_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b7': {
        'display_name': 'EfficientNet-B7',
        'backbone_args': {'efficientnet': {'version': 7}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b7_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_b8': {
        'display_name': 'EfficientNet-B8',
        'backbone_args': {'efficientnet': {'version': 8}},
        'pretrained_parameters': {
            'natural_rgb': 'tensorflow/natural_rgb/efficientnet_b8_advprop-classification-imagenet2012-2017.tar.gz'
        }
    },
    'efficientnet_l2': {
        'display_name': 'EfficientNet-L2',
        'backbone_args': {'efficientnet': {'version': 10}},
        'pretrained_parameters': {
            # 'natural_rgb': 'tensorflow/natural_rgb/efficientnet_l2_noisy_student-classification-imagenet2012-2017.tar.gz'
        }
    },
}
