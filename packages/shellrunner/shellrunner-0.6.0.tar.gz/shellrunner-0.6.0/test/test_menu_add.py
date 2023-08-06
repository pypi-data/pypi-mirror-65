import sys
sys.path.append("..")

import pytest

from shellrunner.menu import Menu

class TestMenuAdd(object):

    def test_add_duplicate_entry(self):
        name = "a-menu"
        existing_command = "existing_command"
        new_command = "new_command"
        # The fast the commands differ should not affect anything

        raw = [
            { name: existing_command },
            { "c-menu": "c-command" }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(ValueError):
            menu.add_command([Menu.HERE], name, new_command)

        with pytest.raises(ValueError):
            menu.add_sub_menu([Menu.HERE], name)

    def test_add_top_level_command(self):
        raw = [
            { "a-menu": "a-command" },
            { "c-menu": "c-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-menu"
        new_command = "b-command"

        with pytest.raises(IndexError):
            menu.select_command([new_name])

        menu.add_command([Menu.HERE], new_name, new_command)

        name, command = menu.select_command([ new_name ])
        assert name    == new_name
        assert command == new_command

    def test_add_menu_and_nested_command(self):
        raw = [
            { "a-menu": "a-command" },
            { "c-menu": "c-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-nested"
        new_command = "b-command"
        new_sub_menu = "b-menu"

        with pytest.raises(IndexError):
            menu.select_command([new_sub_menu])

        menu.add_sub_menu([Menu.HERE], new_sub_menu)
        menu.add_command([new_sub_menu, Menu.HERE], new_name, new_command)

        name, command = menu.select_command([new_sub_menu, new_name])
        assert name    == new_name
        assert command == new_command

    def test_add_nested_command_by_index(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "*-*"
        new_command = "==SOMETHING=="

        menu.add_command(["2", "1"], new_name, new_command)

        name, command = menu.select_command(["2", "1", "2"])
        assert name    == new_name
        assert command == new_command

    def test_add_nested_command_by_match(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "LOVE"
        new_command = "Tutik"

        menu.add_command(["b", "_", Menu.HERE], new_name, new_command)

        name, command = menu.select_command(["b", "_", "LOVE"])
        assert name    == new_name
        assert command == new_command
