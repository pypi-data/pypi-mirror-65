import copy

from .common import common_config

c = copy.deepcopy(common_config)
c['meta_arch_default_args']['classification_loss'] = {'weighted_sigmoid': {}}

configs = {
    'Sigmoid': c
}

