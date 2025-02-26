import os

from . import _config

INPUT_PATH = os.sep.join(_config.get('media', 'input_path_dir').split('.'))
OUTPUT_PATH = os.sep.join(_config.get('media', 'output_path_dir').split('.'))

os.makedirs(INPUT_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)
