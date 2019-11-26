from abc import ABC
from pathlib import Path

import yaml


class App(ABC):
    def __init__(self, config_name: str = None):
        self.config = None
        self._set_config(config_name)

    def _set_config(self, config_name: str):
        default_file = Path.cwd() / 'config.yaml'

        with open(default_file, 'r') as f:
            self.config = yaml.safe_load(f)

        cf_dict = {}
        if config_name:
            cf_dict = yaml.safe_load(config_name)

        self.config.update(**cf_dict)