import sys
sys.path.append("..")

import pytest

from shellrunner.menu import Menu

class TestMenuRemove(object):

    def test_remove_inexistant_command_by_index(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(IndexError):
            menu.remove(indexes=[ 3 ])

    def test_remove_inexistant_command_by_match(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(IndexError):
            menu.remove(matches=[ "@" ])

    def test_remove_last_top_level_command_by_index(self):
        raw = [
            { "a-menu": "a-command" }
        ]
        menu = Menu(raw, interactive=False)

        menu.remove(indexes=[ 1 ])

        with pytest.raises(IndexError):
            menu.select_command(indexes=[ 1 ])

    def test_remove_top_level_command_by_match(self):
        raw = [
            { "a-menu": "a-command" },
            { "c-menu": "c-command" }
        ]
        menu = Menu(raw, interactive=False)

        menu.remove(matches=[ "a" ])

        with pytest.raises(IndexError):
            menu.select_command(matches=[ "a" ])

    def test_remove_nested_command_by_index(self):
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

        menu.remove(indexes=[ 2, 1, 2 ])

        with pytest.raises(IndexError):
            menu.select_command(indexes=[ 2, 1, 2 ])

    def test_remove_nested_command_by_match(self):
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

        menu.remove(matches=[ "b", "_", "3" ])

        with pytest.raises(IndexError):
            menu.select_command(matches=[ "b", "_", "3" ])

    def test_remove_empty_sub_menu_by_match(self):
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

        menu.remove(matches=[ "b", "_", "^" ])

        with pytest.raises(IndexError):
            menu.select_command(matches=[ "b", "_", "^" ])

    def test_remove_non_empty_sub_menu_without_force_fails(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" },
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        with pytest.raises(ValueError):
            menu.remove(matches=[ "b", "_" ])

    def test_remove_non_empty_sub_menu_with_force_succeeds(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" },
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        menu.remove(matches=[ "b" ], force=True)

        with pytest.raises(IndexError):
            menu.select_command(matches=[ "b", "_", "3" ])

    def test_remove_top_level_with_force_succeeds(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" },
                    { "3-cmd": "value_3.3" },
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        assert menu.raw == raw
        menu.remove(matches=[ "." ], force=True)
        assert menu.raw == []
