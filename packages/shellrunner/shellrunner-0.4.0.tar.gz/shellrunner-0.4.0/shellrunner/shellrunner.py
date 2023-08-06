#!/usr/bin/env python3

import sys
import argparse
import traceback

from .config import Config
from .runner import Runner
from .menu import Menu

def run(args):
    # argparse appends all the arguments, so we have to reverse the arguments
    # to use them as a queue (fifo), not a stack (lifo).
    args.indexes.reverse()
    args.matches.reverse()

    conf = Config()
    menu = Menu(conf.commands)
    description, command = menu.select_command(args.indexes, args.matches)
    Runner.execute(command)

def add_sub_menu(args):
    # argparse appends all the arguments, so we have to reverse the arguments
    # to use them as a queue (fifo), not a stack (lifo).
    args.indexes.reverse()
    args.matches.reverse()

    conf = Config()
    menu = Menu(conf.commands)
    menu.add_sub_menu(args.description, args.indexes, args.matches)
    conf.set_commands(menu.entries)
    conf.save()

def add_command(args):
    # argparse appends all the arguments, so we have to reverse the arguments
    # to use them as a queue (fifo), not a stack (lifo).
    args.indexes.reverse()
    args.matches.reverse()

    conf = Config()
    menu = Menu(conf.commands)
    menu.add_command(args.description, args.command, args.indexes, args.matches)
    conf.set_commands(menu.entries)
    conf.save()

def edit(args):
    conf = Config()
    editor = args.editor if args.editor else conf.editor
    Runner.execute('{} {}'.format(editor, conf.file))

def config(args):
    conf = Config()
    for k, v in conf.general.items():
        print('{} = {}'.format(k, v))

def add_selection_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--indexes', nargs='*', default=[], type=int)
    group.add_argument('-m', '--matches', nargs='*', default=[], type=str)

def add_run_menu(subparsers):
    run_parser = subparsers.add_parser('run', help="Run a command")
    add_selection_arguments(run_parser)
    run_parser.set_defaults(func=run)

def add_add_menu(subparsers):
    add_parser = subparsers.add_parser('add', help="Add a command to configuration")
    add_subparsers = add_parser.add_subparsers(title="Entry", dest='entry')

    add_command_parser = add_subparsers.add_parser('command', help="Add a command")
    add_selection_arguments(add_command_parser)
    add_command_parser.add_argument('description', help="Command description")
    add_command_parser.add_argument('command', help="Raw command")
    add_command_parser.set_defaults(func=add_command)

    add_menu_parser = add_subparsers.add_parser('sub_menu', help="Add a sub-menu")
    add_selection_arguments(add_menu_parser)
    add_menu_parser.add_argument('description', help="Menu description")
    add_menu_parser.set_defaults(func=add_sub_menu)

def add_edit_menu(subparsers):
    edit_parser = subparsers.add_parser('edit', help="Edit configuration")
    edit_parser.add_argument('-e', '--editor', required=False, type=str)
    edit_parser.set_defaults(func=edit)

def add_config_menu(subparsers):
    config_parser = subparsers.add_parser('config', help="Print configuration")
    config_parser.set_defaults(func=config)

def main():
    parser = argparse.ArgumentParser(prog='ShellRunner')
    subparsers = parser.add_subparsers(title="Actions", dest='action')

    add_run_menu(subparsers)
    add_add_menu(subparsers)
    add_edit_menu(subparsers)
    add_config_menu(subparsers)

    # If no subparser is specified (must be the first argument),
    # use 'run' as default
    if sys.argv[1] not in subparsers.choices.keys():
        sys.argv.insert(1, 'run')

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    sys.exit(main())
