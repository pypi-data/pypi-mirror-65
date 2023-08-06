'''Defines the Config class
'''

import os
import json
import hashlib

class Config(object):
    '''Manages the configuration for the project
    '''

    __GENERAL = 'config'

    __EDITOR = 'editor'
    __EDITOR_DEFAULT = 'vim'

    __COMMANDS = 'commands'

    __FILENAME = 'config.json'
    __DIRNAME = '.shellrunner'

    def __init__(self):
        self.__dir = os.path.join(os.path.expanduser('~'), self.__DIRNAME)
        self.__file = os.path.join(self.__dir, self.__FILENAME)

        self.__load()

    def __default(self):
        return {
            self.__GENERAL: {
                self.__EDITOR: self.__EDITOR_DEFAULT
            },
            self.__COMMANDS: [
                {
                    'vibash': 'vi ~/.bashrc'
                },
                {
                    'monitor': [
                        { 'top': 'top' },
                        { 'cpu': 'ps aux | awk \'{ if ($3 == "%CPU" || $3 > 10.0) print }\'' }
                    ]
                }
            ]
        }

    def __init(self):
        if not os.path.isdir(self.__dir):
            os.mkdir(self.__dir)

        if not os.path.isfile(self.__file):
            self.__save(self.__default(), True)

    def __save(self, config, force=False):
        if not force:
            with open(self.__file, 'rb') as fp:
                current_hash = hashlib.md5(fp.read()).hexdigest()
                if current_hash != self.__hash:
                    raise ValueError(
                        'Configuration file changed since we loaded it, aborting!')

        with open(self.__file, 'w') as fp:
            json.dump(config, fp, indent=2)

    def save(self):
        self.__save(self.__config)

    def __load(self):
        if not os.path.isfile(self.__file):
            self.__init()

        with open(self.__file) as fp:
            data = fp.read()
            self.__config = json.loads(data)
            self.__hash = hashlib.md5(data.encode()).hexdigest()

    def set_commands(self, commands):
        self.__config[self.__COMMANDS] = commands

    @property
    def commands(self):
        return self.__config[self.__COMMANDS]

    @property
    def general(self):
        return self.__config[self.__GENERAL]

    @property
    def editor(self):
        return self.general[self.__EDITOR]

    @property
    def file(self):
        return self.__file

if __name__ == '__main__':
    conf = Config()
    print(conf.commands)
    print(conf.general)

