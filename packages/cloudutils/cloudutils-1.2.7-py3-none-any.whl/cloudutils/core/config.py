# Copyright © 2019 Noel Kaczmarek
import json
import os


class ConfigError(Exception):
    pass

class ConfigLockError(ConfigError):
    pass

class ConfigReadError(ConfigError):
    pass


class Config(dict):
    def __init__(self, init={}, name=None):
        name = name or self.__class__.__name__.lower()
        dict.__init__(self, init)
        dict.__setattr__(self, '_locked', 0)
        dict.__setattr__(self, '_name', name)

    def __setitem__(self, key, value):
        if self._locked and not key in self:
            raise ConfigLockError('Setting attribute on locked config')
        return super(Config, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(Config, self).__getitem__(name)

    def __delitem__(self, name):
        return super(Config, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def lock(self):
        dict.__setattr__(self, '_locked', 1)

    def unlock(self):
        dict.__setattr__(self, '_locked', 0)

    def islocked(self):
        return self._locked

    def copy(self):
        config = Config(self)
        if self.islocked():
            config.lock()
        return config


def load(file):
    try:
        if os.path.isfile(file):
            with open(file) as f:
                return json.load(f)
        raise Exception('File not found')
    except Exception as e:
        print('Error while loading config: ', e)
        exit()


def save(file, config):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Error while saving config to \'%s\': %s' % (file, e))
