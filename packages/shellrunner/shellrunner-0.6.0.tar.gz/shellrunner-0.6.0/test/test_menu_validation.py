import sys
sys.path.append("..")

import pytest

from shellrunner.menu import Menu

class TestMenuValidation(object):

    def test_invalid_top_level(self):
        with pytest.raises(ValueError):
            raw = { "command": "ps aux" }
            menu = Menu(raw)

    def test_invalid_sub_menu(self):
        with pytest.raises(ValueError):
            raw = [
                { "command": "ps aux" },
                { "submenu": {
                    "subcmd": "top"
                } }
            ]
            menu = Menu(raw)

    def test_invalid_command(self):
        with pytest.raises(ValueError):
            raw = [
                { "command": "ps aux" },
                { "submenu": [
                    { "subcmd": None }
                ] }
            ]
            menu = Menu(raw)

    def test_valid(self):
        raw = [
            { "a-menu": [
                { "1-cmd": "value_1.1" }
            ] },
            { "b-menu": [
                { "_123_": [
                    { "2-cmd": "value_2.2" }
                ] }
            ] },
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
        menu = Menu(raw)
