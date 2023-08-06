#!/usr/bin/env python3

import sys
import argparse
import traceback

from .config import Config
from .runner import Runner
from .menu import Menu

def run(args):
    conf = Config()
    menu = Menu(conf.commands)
    _, command = menu.select_command(args.selection)
    for arg in args.selection:
        command += " " + arg
    Runner.execute(command)

def add_sub_menu(args):
    conf = Config()
    menu = Menu(conf.commands)
    menu.add_sub_menu(args.selection, args.name)
    conf.set_commands(menu.raw).save()

def add_command(args):
    conf = Config()
    menu = Menu(conf.commands)
    menu.add_command(args.selection, args.name, args.command)
    conf.set_commands(menu.raw).save()

def remove(args):
    conf = Config()
    menu = Menu(conf.commands)
    menu.remove(args.selection, force=args.force)
    conf.set_commands(menu.raw).save()

def edit(args):
    conf = Config()
    menu = Menu(conf.commands)
    menu.edit(args.selection, args.name, args.command)
    conf.set_commands(menu.raw).save()

def config_edit(args):
    conf = Config()
    editor = args.editor if args.editor else conf.editor
    Runner.execute("{} {}".format(editor, conf.file))

def config_print(args):
    conf = Config()
    for k, v in conf.general.items():
        print("{} = {}".format(k, v))

def add_selection_arguments(parser):
    parser.add_argument("selection", nargs="*", type=str)

def add_run_menu(subparsers):
    run_parser = subparsers.add_parser("run", help="Run a command")
    run_parser.set_defaults(func=run)
    add_selection_arguments(run_parser)

def add_add_menu(subparsers):
    add_parser = subparsers.add_parser("add", help="Add entry")
    add_subparsers = add_parser.add_subparsers(title="Type", dest="type")

    add_command_parser = add_subparsers.add_parser("command", help="Add a command")
    add_command_parser.set_defaults(func=add_command)
    add_command_parser.add_argument("name", help="Command name")
    add_command_parser.add_argument("command", help="Command")
    add_selection_arguments(add_command_parser)

    add_menu_parser = add_subparsers.add_parser("sub_menu", help="Add a sub-menu")
    add_menu_parser.set_defaults(func=add_sub_menu)
    add_menu_parser.add_argument("name", help="Menu name")
    add_selection_arguments(add_menu_parser)

def add_remove_menu(subparsers):
    remove_parser = subparsers.add_parser("remove", help="Remove entry")
    remove_parser.set_defaults(func=remove)
    remove_parser.add_argument("-f", "--force", required=False, action="store_true")
    add_selection_arguments(remove_parser)

def add_edit_menu(subparsers):
    edit_parser = subparsers.add_parser("edit", help="Edit entry")
    edit_parser.set_defaults(func=edit)
    edit_parser.add_argument("-n", "--name", required=False,
            default=None, type=str)
    edit_parser.add_argument("-c", "--command", required=False,
            default=None, type=str)
    add_selection_arguments(edit_parser)

def add_config_menu(subparsers):
    config_parser = subparsers.add_parser("config", help="Print configuration")
    config_subparsers = config_parser.add_subparsers(
            title="Sub-action", dest="sub_action")

    config_print_parser = config_subparsers.add_parser("print", help="Print config")
    config_print_parser.set_defaults(func=config_print)

    config_edit_parser = config_subparsers.add_parser("edit", help="Edit config")
    config_edit_parser.add_argument("-e", "--editor", required=False, type=str)
    config_edit_parser.set_defaults(func=config_edit)

def main():
    parser = argparse.ArgumentParser(prog="ShellRunner")
    subparsers = parser.add_subparsers(title="Actions", dest="action")

    add_run_menu(subparsers)
    add_add_menu(subparsers)
    add_remove_menu(subparsers)
    add_edit_menu(subparsers)
    add_config_menu(subparsers)

    # If no subparser is specified (must be the first argument),
    # use "run" as default
    if len(sys.argv) < 2 or sys.argv[1] not in subparsers.choices.keys():
        sys.argv.insert(1, "run")

    try:
        args = parser.parse_args()
        args.func(args)
    except KeyboardInterrupt as ex:
        print('\nAborted!')
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    sys.exit(main())
