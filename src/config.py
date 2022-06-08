import json
import ntpath
from os import stat
from dataclasses import dataclass


@dataclass
class Config(object):
    config_dir = './config.json'
    defaults = {
        "Obfuscate": True,
        "AntiDebug": True,
        "AntiDecompile": True,
        "DeadCode": True,
        "Marshal": True,
        "Minify": True,
        "EncryptBytecode": True,
        "SignExecutable": False,
        "LayerAmount": 1
    }

    def __init__(self):
        self.config_dir = self.__class__.config_dir
        self.defaults = self.__class__.defaults

        if not ntpath.exists(self.config_dir):
            print(f'config.json not found! Creating one --> {self.config_dir}')
            self.create_config()

        if stat(self.config_dir).st_size == 0:
            print(f'config.json is empty! Applying defaults --> {self.config_dir}')
            self.create_config()

    def create_config(self):
        with open(self.config_dir, 'w') as f:
            json.dump(
                self.defaults, f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True
            )

    @classmethod
    def get_setting(cls, setting):
        with open(cls.config_dir) as json_:
            data = json.load(json_)
        # if the config has empty dict in it
        if not bool(data):
            print(f'config.json is empty! Applying defaults --> {cls.config_dir}')
            cls.create_config()
        try:
            key = data.get(setting)
        except KeyError:
            key = 'no key named ' + setting
        return key
