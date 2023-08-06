#!/usr/bin/env python3

import sys
import argparse
import traceback

from .db import Database
from .runner import Runner
from .menu import Menu

def run(args):
    # argparse appends all the arguments, so we have to reverse the arguments
    # to use them as a queue (fifo), not a stack (lifo).
    args.indexes.reverse()
    args.matches.reverse()

    commands = Database.get_commands()
    menu = Menu(commands)
    description, command = menu.select(args.indexes, args.matches)

    print('Running \'{}\' [{}]'.format(description, command))
    Runner.execute(command)

def edit(args):
    Database.edit_config()

def config(args):
    config = Database.get_config()
    for k, v in config.items():
        print('{} = {}'.format(k, v))

def main():
    parser = argparse.ArgumentParser(prog='ShellRunner')
    subparsers = parser.add_subparsers(title="Actions", dest='action')

    run_parser = subparsers.add_parser('run', help="Run a command")
    quick_match_group = run_parser.add_mutually_exclusive_group()
    quick_match_group.add_argument('-i', '--indexes', nargs='*', default=[], type=int)
    quick_match_group.add_argument('-m', '--matches', nargs='*', default=[], type=str)
    run_parser.set_defaults(func=run)

    edit_parser = subparsers.add_parser('edit', help="Edit configuration")
    edit_parser.set_defaults(func=edit)

    config_parser = subparsers.add_parser('config', help="Print configuration")
    config_parser.set_defaults(func=config)

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception as ex:
        traceback.print_exc()

if __name__ == '__main__':
    sys.exit(main())
