import sys
sys.path.append("..")

import pytest

from shellrunner.menu import Menu

class TestMenuRemove(object):

    def test_edit_inexistant_command_by_match(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(IndexError):
            menu.edit(["@"], name="b-menu")

    def test_edit_top_level_command_name_by_index(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-menu"
        menu.edit(["1"], name=new_name)

        name, command = menu.select_command(["1"])
        assert name == new_name

    def test_edit_top_level_command_name_and_value_by_match(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-menu"
        new_command = "b-command"
        menu.edit(["a"], name=new_name, value=new_command)

        name, command = menu.select_command(["b"])
        assert name    == new_name
        assert command == new_command

    def test_edit_nested_command_value_by_match(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "%$#@"

        # Without the dash, will select 3rd index
        menu.edit(["b", "_", "3-"], name=new_name)

        name, command = menu.select_command(["b", "_", "%"])
        assert name    == new_name
        assert command == "value_3.3"

    def test_edit_nested_command_value_by_index(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        new_command = "new"
        menu.edit(["2", "1", "1"], value=new_command)

        print(menu.raw)
        name, command = menu.select_command(["2", "1", "1"])
        assert name    == "2-cmd"
        assert command == new_command

    def test_edit_nested_command_name_and_value_by_index(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "%$#@"
        new_command = "lost"
        menu.edit(["2", "1", "1"], name=new_name, value=new_command)

        name, command = menu.select_command(["2", "1", "1"])
        assert name    == new_name
        assert command == new_command

    def test_edit_sub_menu_name(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" },
                    { "^menu^": [] }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(ValueError):
            menu.edit(["b", "_", "^"], value="something")

    def test_empty_edit(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" },
                    { "^menu^": [] }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(ValueError):
            menu.edit(["b", "_", "2-cmd"])
