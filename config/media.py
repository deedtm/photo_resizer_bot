import os

from . import _config

INPUT_PATH = os.sep.join(_config.get('media', 'input_path_dir').split('.'))
OUTPUT_PATH = os.sep.join(_config.get('media', 'output_path_dir').split('.'))
