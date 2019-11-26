from abc import ABC
from pathlib import Path

import yaml


class App(ABC):
    """
    Basic class for web application
    """
    def __init__(self, config_name: str = None):
        self.config = None
        self._set_config(config_name)

    def __load_config(self, file):
        with open(file, 'r') as f:
            self.config = yaml.safe_load(f)

    def _set_config(self, config_name: str):
        """
        Set constants from configuration file
        :param config_name: str
        :return: None
        """

        try:
            self.__load_config(Path.cwd() / 'config.yaml')
        except FileNotFoundError:
            self.__load_config(Path.cwd().parent / 'config.yaml')

        cf_dict = {}
        if config_name:
            cf_dict = yaml.safe_load(config_name)

        self.config.update(**cf_dict)