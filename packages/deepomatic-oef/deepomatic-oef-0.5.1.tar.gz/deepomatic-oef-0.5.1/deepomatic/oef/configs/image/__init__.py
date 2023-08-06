from . import classification
from . import detection
from . import ocr

modules = [classification, detection, ocr]

configs = {}
for m in modules:
    configs['image_' + m.__name__.split('.')[-1]] = m.configs
