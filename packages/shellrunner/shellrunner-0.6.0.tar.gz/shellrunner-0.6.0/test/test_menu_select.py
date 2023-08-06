import sys
sys.path.append("..")

import pytest

import itertools

from shellrunner.menu import Menu

class TestMenuSelect(object):

    def test_select_with_numbers_fail(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        menu = Menu(raw, interactive=False)
        with pytest.raises(ValueError):
            menu.select_command([3])

    def test_select_with_non_list_fails(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        menu = Menu(raw, interactive=False)
        with pytest.raises(ValueError):
            menu.select_command("3")

    def test_select_top_level_command_numeric(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        menu = Menu(raw, interactive=False)
        name, command = menu.select_command(["3"])
        assert name    == "top"
        assert command == "gear"

    def test_select_top_level_command_textual(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        for permutation in itertools.permutations(raw):
            menu = Menu(raw, interactive=False)
            name, command = menu.select_command(["top"])
            assert name    == "top"
            assert command == "gear"

    def test_select_top_level_command_with_extra_arguments(self):
        raw = [
            { "bottom": "half" },
            { "middle": "ground" },
            { "top": "gear" }
        ]
        for permutation in itertools.permutations(raw):
            menu = Menu(raw, interactive=False)
            selection = ["top", "-ef", "sort"]
            name, command = menu.select_command(selection)
            assert name      == "top"
            assert command   == "gear"
            assert selection == ["-ef", "sort"]


    def test_select_nested_command(self):
        raw = [
            { "top-level-command": "top_level_command" },
            { "c-menu": [
                { "(_._)": [
                    { "*": [
                        { "2-cmd": "value_of_\"2-cmd\"" },
                        { "1-cmd": "value_of_'1-cmd'" },
                        { "0-cmd": "value_of_0-cmd" }
                    ] }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        name, command = menu.select_command(["2", "(_.", "*", "1-"])
        assert name    == "1-cmd"
        assert command == "value_of_'1-cmd'"

        name, command = menu.select_command(["2", "(_.", "*", "1"])
        assert name    == "2-cmd"
        assert command == "value_of_\"2-cmd\""

    def test_select_nested_command_with_extra_arguments(self):
        raw = [
            { "top-level-command": "top_level_command" },
            { "c-menu": [
                { "(_._)": [
                    { "*": [
                        { "2-cmd": "value_of_\"2-cmd\"" },
                        { "1-cmd": "value_of_'1-cmd'" },
                        { "0-cmd": "value_of_0-cmd" }
                    ] }
                ] }
            ] }
        ]
        menu = Menu(raw, interactive=False)

        selection = ["2", "(_.", "*", "1-", "start", "all", "-it"]
        name, command = menu.select_command(selection)
        assert name      == "1-cmd"
        assert command   == "value_of_'1-cmd'"
        assert selection == ["start", "all", "-it"]

        selection = ["2", "(_.", "*", "1", "start", "all", "-it"]
        name, command = menu.select_command(selection)
        assert name    == "2-cmd"
        assert command == "value_of_\"2-cmd\""
        assert selection == ["start", "all", "-it"]

    def test_select_top_level_non_existant_command_by_index(self):
        raw = [
            { "a-menu": "command" }
        ]
        menu = Menu(raw, interactive=False)
        with pytest.raises(IndexError):
            menu.select_command([str(len(raw) + 1)])

    def test_select_top_level_non_existant_command_by_match(self):
        raw = [
            { "a-menu": "command" }
        ]
        menu = Menu(raw, interactive=False)
        with pytest.raises(IndexError):
            menu.select_command(["@"])

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
        with pytest.raises(IndexError):
            menu.select_command(["1", "4"])

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
        with pytest.raises(IndexError):
            menu.select_command(["b", "@"])
