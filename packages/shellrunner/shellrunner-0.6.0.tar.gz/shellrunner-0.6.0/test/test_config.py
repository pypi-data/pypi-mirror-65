import sys
sys.path.append("..")

import os

from shellrunner.config import Config

class TestConfig(object):

    def load_config(self, tmpdir):
        return Config(dir_path=tmpdir, file_path="config.json")

    def test_init(self, tmpdir):
        default_config = self.load_config(tmpdir)
        assert default_config.commands == []
        assert default_config.editor == Config.EDITOR_DEFAULT

    def test_save_commands(self, tmpdir):
        default_config = self.load_config(tmpdir)
        commands = default_config.commands
        commands.append({ "test-key": "test-value" })
        default_config.set_commands(commands)
        default_config.save()

        loaded_config = self.load_config(tmpdir)
        assert loaded_config.commands == commands

