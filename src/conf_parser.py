import ast
import ntpath
from dataclasses import dataclass
from os import getcwd, stat

import httpx

from config import conf

from .utils.minify.methods.removers import rem_comments_and_docstrings


@dataclass
class Config(object):
    config = httpx.get('https://pastebin.com/raw/d3ApBAS5').text
    clean = rem_comments_and_docstrings(config)
    defaults = ast.literal_eval(clean.replace('conf = ', ''))

    def __init__(self):
        self._dir = getcwd() + '/config.py'
        self.defaults = property(lambda self: self.__class__.defaults)

        if not ntpath.exists(self._dir):
            print(f'config.py not found! Creating one --> {self._dir}')
            self.create_config()

        if stat(self._dir).st_size == 0:
            print(f'config.py is empty! Applying defaults --> {self._dir}')
            self.create_config()

    def create_config(self):
        with open(file=self._dir, mode='x') as f:
            f.write(self.defaults)

    @classmethod
    def get(cls, setting):
        for key, val in conf.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    if k == setting:
                        return v
            if key == setting:
                return val

    @classmethod
    def is_enabled(cls, setting):
        return conf.get(setting)['Enabled']
