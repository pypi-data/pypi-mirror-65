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
            menu.edit(name="b-menu", matches=[ "@" ])

    def test_edit_top_level_command_name_by_index(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-menu"
        menu.edit(name=new_name, indexes=[ 1 ])

        name, command = menu.select_command(indexes=[ 1 ])
        assert name == new_name

    def test_edit_top_level_command_name_and_value_by_match(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-menu"
        new_command = "b-command"
        menu.edit(name=new_name, value=new_command, matches=[ "a" ])

        name, command = menu.select_command(matches=[ "b" ])
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
        menu.edit(name=new_name, matches=[ "b", "_", "3" ])

        name, command = menu.select_command(matches=[ "b", "_", "%" ])
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
        menu.edit(value=new_command, indexes=[ 2, 1, 1 ])

        print(menu.raw)
        name, command = menu.select_command(indexes=[ 2, 1, 1 ])
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
        menu.edit(name=new_name, value=new_command, indexes=[ 2, 1, 1 ])

        name, command = menu.select_command(indexes=[ 2, 1, 1 ])
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
            menu.edit(value="something", matches=[ "b", "_", "^" ])

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
            menu.edit(matches=[ "b", "_", "3" ])
