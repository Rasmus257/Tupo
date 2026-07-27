from config import conf

# Snapshot of the option set, taken at import time (before main.py mutates
# `conf` at runtime). Only the top-level section keys are read downstream, to
# know which obfuscation stages exist.
_DEFAULTS = dict(conf)


class Config:
    defaults = _DEFAULTS

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
        try:
            return conf.get(setting)['Enabled']
        except (KeyError, TypeError):
            return False
