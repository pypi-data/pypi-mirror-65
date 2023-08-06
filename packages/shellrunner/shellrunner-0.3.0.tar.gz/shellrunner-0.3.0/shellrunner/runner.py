import os

class Runner(object):

    __SHELL = '/bin/bash'

    @staticmethod
    def execute(command):
        if not command:
            raise RuntimeError('Cannot execute an empty command')

        args = [Runner.__SHELL, '-c', command]
        os.execv(args[0], args)
