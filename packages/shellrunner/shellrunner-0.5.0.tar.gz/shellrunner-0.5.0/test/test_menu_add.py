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
            menu.add_command(name, new_command, matches=[ Menu.HERE ])

        with pytest.raises(ValueError):
            menu.add_sub_menu(name, matches=[ Menu.HERE ])

    def test_add_top_level_command(self):
        raw = [
            { "a-menu": "a-command" },
            { "c-menu": "c-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_name = "b-menu"
        new_command = "b-command"

        with pytest.raises(IndexError):
            menu.select_command(matches=[ new_name ])

        menu.add_command(new_name, new_command, matches=[ Menu.HERE ])
        name, command = menu.select_command(matches=[ new_name ])
        assert name    == new_name
        assert command == new_command

    def test_add_menu_and_nested_command(self):
        raw = [
            { "a-menu": "a-command" },
            { "c-menu": "c-command" }
        ]
        menu = Menu(raw, interactive=False)

        new_sub_menu = "b-menu"
        new_name = "b-nested"
        new_command = "b-command"

        with pytest.raises(IndexError):
            menu.select_command(matches=[ new_sub_menu ])

        menu.add_sub_menu(new_sub_menu, matches=[ Menu.HERE ])
        menu.add_command(new_name, new_command,
                         matches=[ new_sub_menu, Menu.HERE ])

        command_match = [ new_sub_menu, new_name ]
        name, command = menu.select_command(matches=command_match)
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

        add_indexes = [ 2, 1 ]
        select_indexes = [ 2, 1, 2 ] # Command is appended

        menu.add_command(new_name, new_command, indexes=add_indexes)

        name, command = menu.select_command(indexes=select_indexes)
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

        add_matches = [ "b", "_", Menu.HERE ]
        select_matches = [ "b", "_", "LOV" ]

        menu.add_command(new_name, new_command, matches=add_matches)

        name, command = menu.select_command(matches=select_matches)
        assert name    == new_name
        assert command == new_command
