from . import meta_archs

modules = [meta_archs]

config_items = []
for m in modules:
    config_items += list(m.configs.items())

configs = dict(config_items)

assert len(configs) == len(config_items)
