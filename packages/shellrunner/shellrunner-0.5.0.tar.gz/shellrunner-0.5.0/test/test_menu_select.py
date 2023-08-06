import sys
sys.path.append("..")

import pytest

import itertools

from shellrunner.menu import Menu

class TestMenuSelect(object):

    def test_select_using_both_indexes_and_matches(self):
        raw = [
            { "command": "ps aux" },
            { "submenu": [
                { "subcmd": "top" }
            ] }
        ]
        menu = Menu(raw)
        with pytest.raises(ValueError):
            indexes = [ 1 ]
            matches = [ "c" ]
            menu.select_command(indexes=indexes, matches=matches)

    def test_select_top_level_command_by_index(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        menu = Menu(raw, interactive=False)
        indexes = [ 3 ]
        name, command = menu.select_command(indexes=indexes)
        assert name    == "top"
        assert command == "gear"

    def test_select_top_level_command_by_match(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        for permutation in itertools.permutations(raw):
            menu = Menu(raw, interactive=False)
            matches = [ "top" ]
            name, command = menu.select_command(matches=matches)
            assert name    == "top"
            assert command == "gear"

    def test_select_nested_command_by_index(self):
        raw = [
            { "top-level-command": "top_level_command" },
            { "c-menu": [
                { "(_._)": [
                    { "!": [
                        { "2-cmd": "value_of_\"2-cmd\"" },
                        { "1-cmd": "value_of_'1-cmd'" },
                        { "0-cmd": "value_of_0-cmd" }
                    ] }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)
        indexes = [ 2, 1, 1, 3 ]
        name, command = menu.select_command(indexes=indexes)
        assert name    == "0-cmd"
        assert command == "value_of_0-cmd"

    def test_select_nested_command_by_match(self):
        raw = [
            { "top-level-command": "top_level_command" },
            { "c-menu": [
                { "(_._)": [
                    { "!": [
                        { "2-cmd": "value_of_\"2-cmd\"" },
                        { "1-cmd": "value_of_'1-cmd'" },
                        { "0-cmd": "value_of_0-cmd" }
                    ] }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)
        matches = [ "c", "(_.", "!", "1" ]
        name, command = menu.select_command(matches=matches)
        assert name    == "1-cmd"
        assert command == "value_of_'1-cmd'"

    def test_select_top_level_non_existant_command_by_index(self):
        raw = [
            { "a-menu": "command" }
        ]
        menu = Menu(raw, interactive=False)
        indexes = [ len(raw) + 1 ]
        with pytest.raises(IndexError):
            menu.select_command(indexes, [])

    def test_select_top_level_non_existant_command_by_match(self):
        raw = [
            { "a-menu": "command" }
        ]
        menu = Menu(raw, interactive=False)
        matches = [ "@" ]
        with pytest.raises(IndexError):
            menu.select_command(matches=matches)

    def test_select_nested_non_existant_command_by_index(self):
        raw = [
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" }
                ] },
                { "4_5_6": "something" }
            ] }
        ]
        menu = Menu(raw, interactive=False)
        indexes = [ 1, 4 ]
        with pytest.raises(IndexError):
            menu.select_command(indexes=indexes)

    def test_select_nested_non_existant_command_by_match(self):
        raw = [
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" }
                ] },
                { "4_5_6": "something" }
            ] }
        ]
        menu = Menu(raw, interactive=False)
        matches = [ "b", "@" ]
        with pytest.raises(IndexError):
            menu.select_command(matches=matches)
