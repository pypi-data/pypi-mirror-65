backbones = [
    {
        'display_name': 'LeNet',
        'backbone_args': {'net': 0},
    },
    {
        'display_name': 'AlexNet',
        'backbone_args': {'net': 1},
    },
    {
        'display_name': 'OverFeat',
        'backbone_args': {'net': 3},
    },
    {
        'display_name': 'VGG A',
        'backbone_args': {'net': 4},
    },
    {
        'display_name': 'VGG 16',
        'backbone_args': {'net': 5},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/vgg_16-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'VGG 19',
        'backbone_args': {'net': 6},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/vgg_19-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'Inception v1',
        'backbone_args': {'net': 7},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'Inception v2',
        'backbone_args': {'net': 8},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v2-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'Inception v3',
        'backbone_args': {'net': 9},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v3-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'Inception v4',
        'backbone_args': {'net': 10},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_v4-classification-imagenet2012-2016_09_09.ckpt'
        },
    },
    {
        'display_name': 'Inception ResNet v2',
        'backbone_args': {'net': 11},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/inception_resnet_v2-classification-imagenet2012-2016_08_30.ckpt'
        },
    },
    {
        'display_name': 'ResNet 50 v1',
        'backbone_args': {'net': 12},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_50_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'ResNet 101 v1',
        'backbone_args': {'net': 13},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_101_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'ResNet 152 v1',
        'backbone_args': {'net': 14},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_152_v1-classification-imagenet2012-2016_08_28.ckpt'
        },
    },
    {
        'display_name': 'ResNet 200 v1',
        'backbone_args': {'net': 15},
    },
    {
        'display_name': 'ResNet 50 v2',
        'backbone_args': {'net': 16},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_50_v2-classification-imagenet2012-2017_04_14.ckpt'
        },
    },
    {
        'display_name': 'ResNet 101 v2',
        'backbone_args': {'net': 17},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_101_v2-classification-imagenet2012-2017_04_14.ckpt'
        },
    },
    {
        'display_name': 'ResNet 152 v2',
        'backbone_args': {'net': 18},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/resnet_152_v2-classification-imagenet2012-2017_04_14.ckpt'
        },
    },
    {
        'display_name': 'ResNet 200 v2',
        'backbone_args': {'net': 19},
    },
    {
        'display_name': 'MobileNet v1',
        'backbone_args': {'net': 20},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v1-classification-imagenet2012-2018_02_22.tar.gz'
        },
    },
    {
        'display_name': 'MobileNet v1 075',
        'backbone_args': {'net': 21},
    },
    {
        'display_name': 'MobileNet v1 050',
        'backbone_args': {'net': 22},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v1_050-classification-imagenet2012-2018_02_22.tar.gz'
        },
    },
    {
        'display_name': 'MobileNet v1 025',
        'backbone_args': {'net': 23},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v1_025-classification-imagenet2012-2018_02_22.tar.gz'
        },
    },
    {
        'display_name': 'MobileNet v2',
        'backbone_args': {'net': 24},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v2-classification-imagenet2012-2018_03_28.tar.gz'
        },
    },
    {
        'display_name': 'MobileNet v2 140',
        'backbone_args': {'net': 25},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/mobilenet_v2_140-classification-imagenet2012-2018_03_28.tar.gz'
        },
    },
    {
        'display_name': 'NasNet Mobile',
        'backbone_args': {'net': 27},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/nasnet_mobile-classification-imagenet2012-2017_10_04.tar.gz'
        },
    },
    {
        'display_name': 'NasNet Large',
        'backbone_args': {'net': 28},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/nasnet_large-classification-imagenet2012-2017_10_04.tar.gz'
        },
    },
    {
        'display_name': 'PNasNet Large',
        'backbone_args': {'net': 29},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/pnasnet_large-classification-imagenet2012-2017_12_13.tar.gz'
        },
    },
    {
        'display_name': 'PNasNet Mobile',
        'backbone_args': {'net': 30},
        'pretrained_weights': {
            'natural_rgb': 'tensorflow/natural_rgb/pnasnet_mobile-classification-imagenet2012-2017_12_13.tar.gz'
        },
    },
    {
        'display_name': 'Darknet 19',
        'backbone_args': {'net': 31},
        'pretrained_weights': {
        },
    },
    {
        'display_name': 'Darknet 53',
        'backbone_args': {'net': 32},
        'pretrained_weights': {
        },
    },
]
