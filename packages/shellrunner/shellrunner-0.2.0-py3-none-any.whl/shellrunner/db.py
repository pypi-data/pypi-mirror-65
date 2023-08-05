import os
import json

from .runner import Runner

class Database(object):

    CONFIG = 'config'

    EDITOR = 'editor'
    EDITOR_DEFAULT = 'vim'

    COMMANDS = 'commands'

    FILENAME = 'config.json'
    DIRNAME = '.shellrunner'

    @classmethod
    def __config_dir(cls):
        home = os.path.expanduser('~')
        return os.path.join(home, cls.DIRNAME)

    @classmethod
    def __config_file(cls):
        config_dir = cls.__config_dir()
        return os.path.join(config_dir, cls.FILENAME)

    @classmethod
    def __config_exists(cls):
        return os.path.isfile(cls.__config_file())

    @classmethod
    def __config_default(cls):
        return {
            cls.CONFIG: {
                cls.EDITOR: cls.EDITOR_DEFAULT
            },
            cls.COMMANDS: [
                'ps aux | grep "example"'
            ]
        }

    @classmethod
    def __init(cls):
        config_dir = cls.__config_dir()
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

        config_file = cls.__config_file()
        if not os.path.isfile(config_file):
            with open(config_file, 'w') as fp:
                json.dump(cls.__config_default(), fp, indent=4)

    @classmethod
    def __load(cls):
        if not cls.__config_exists():
            cls.__init()

        path = cls.__config_file()
        with open(path, 'r') as fp:
            return json.load(fp)

    @classmethod
    def get_commands(cls):
        return cls.__load()[Database.COMMANDS]

    @classmethod
    def get_config(cls):
        return cls.__load()[Database.CONFIG]

    @classmethod
    def edit_config(cls):
        config = cls.get_config()
        editor = config[cls.EDITOR]
        path = cls.__config_file()
        Runner.execute(' '.join([editor, path]))

if __name__ == '__main__':
    commands = Database.get_commands()
    print(commands)
    config = Database.get_config()
    print(config)

