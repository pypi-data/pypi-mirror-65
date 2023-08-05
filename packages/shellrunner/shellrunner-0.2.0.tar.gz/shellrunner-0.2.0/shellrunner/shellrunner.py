#!/usr/bin/env python3

import sys
import argparse
import traceback

from .db import Database
from .runner import Runner

def dict_get_key(d):
    return list(d.keys())[0]

def dict_get_value(d):
    return d[dict_get_key(d)]

def select_from_container(container):
    for i, entry in enumerate(container):
        if isinstance(entry, dict):
            value = dict_get_key(entry)
        elif isinstance(entry, str):
            value = entry
        else:
            raise ValueError('Unexpected nested type:', entry)
        print('{}. {}'.format(i + 1, value))

    print('Please select:', end=' ')

    selection = int(input())
    if selection < 1 or selection > len(container):
        raise IndexError('Bad selection')
    return selection - 1 # Enumerate is indexed 1..N

def __run(commands, index=None):
    if not index:
        index = select_from_container(commands)

    command = commands[index]
    if isinstance(command, dict):
        __run(dict_get_value(command))
    else:
        print('Running \'{}\''.format(command))
        Runner.execute(command)

def run(args):
    commands = Database.get_commands()
    __run(commands, args.index)

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
    run_parser.add_argument('--index', type=int)
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
