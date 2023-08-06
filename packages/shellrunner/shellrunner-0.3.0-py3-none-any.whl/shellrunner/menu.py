'''Defines the Menu class
'''

from .util.dict import get_only_key, get_only_pair

class Menu(object):
    '''A class that represents a structured menu a user can choose from
       either interactively or using predefined arguments.
    '''

    def __init__(self, entries):
        self.__entries = entries
        self.__validate()

    def __validate_sub_menu(self, description, entries):
        if not isinstance(entries, list):
            raise ValueError('Corrupted menu:', description)

        for entry in entries:
            key, value = get_only_pair(entry)
            if isinstance(value, str):
                continue # Valid command structure

            if not isinstance(value, list):
                raise ValueError('Corrupted entry:', key)

            self.__validate_sub_menu(key, value)

    def __validate(self):
        self.__validate_sub_menu('commands', self.__entries)

    def __enumerate_interactive(self, menu):
        for i, entry in enumerate(menu):
            description = get_only_key(entry)
            print('{}. {}'.format(i + 1, description))

    def __select_interactive(self, menu):
        self.__enumerate_interactive(menu)
        print('Please select:', end=' ')
        selection = input()

        try:
            return int(selection) - 1 # Enumerated as 1..N
        except ValueError:
            return self.__select_by_match(menu, selection)

    def __select_by_match(self, menu, match):
        for i, entry in enumerate(menu):
            description = get_only_key(entry)
            if description.startswith(match):
                return i
        raise IndexError('Bad selection:', match)

    def __select(self, menu, indexes, matches):
        if indexes:
            index = indexes.pop() - 1 # Enumerated as 1..N
        elif matches:
            prefix = matches.pop()
            index = self.__select_by_match(menu, matches.pop())
        else:
            index = self.__select_interactive(menu)

        first = 0
        last = len(menu) - 1;
        if not first <= index <= last:
            raise IndexError('Bad selection: {} not in [{}, {}]'.format(index, first, last))

        description, value = get_only_pair(menu[index])
        if isinstance(value, list):
            return self.__select(value, indexes, matches)
        else:
            return description, value

    def select(self, indexes=[], matches=[]):
        return self.__select(self.__entries, indexes, matches)
