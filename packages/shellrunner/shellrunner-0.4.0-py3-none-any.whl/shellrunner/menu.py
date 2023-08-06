'''Defines the Menu class
'''

from .util.dict import get_only_key, get_only_pair

class Menu(object):
    '''A class that represents a structured menu a user can choose from
       either interactively or using predefined arguments.
    '''

    __TOP_LEVEL_DESCRIPTION = 'commands'
    __SELECT_MENU = '.'

    def __init__(self, entries):
        self.__entries = entries
        self.__validate()

    @property
    def entries(self):
        return self.__entries

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
        self.__validate_sub_menu(self.__TOP_LEVEL_DESCRIPTION, self.__entries)

    def __enumerate_interactive(self, menu):
        for i, entry in enumerate(menu):
            description = get_only_key(entry)
            print('{}. {}'.format(i + 1, description))

    def __select_interactive(self, description, menu):
        self.__enumerate_interactive(menu)
        print('Please select:', end=' ')
        selection = input()

        try:
            return int(selection) - 1 # Enumerated as 1..N
        except ValueError:
            return self.__select_by_match(description, menu, selection)

    def __select_by_match(self, description, menu, match):
        if not match or match == self.__SELECT_MENU:
            return self.__SELECT_MENU

        for i, entry in enumerate(menu):
            key = get_only_key(entry)
            if key.startswith(match):
                return i
        raise IndexError("Bad selection: No '{}' in '{}'"
                         .format(match, description))

    def __select(self, description, menu, indexes, matches):
        if indexes:
            index = indexes.pop() - 1 # Enumerated as 1..N
        elif matches:
            index = self.__select_by_match(description, menu, matches.pop())
        else:
            index = self.__select_interactive(description, menu)

        if index == self.__SELECT_MENU:
            return description, menu

        first = 0
        last = len(menu) - 1;
        if not first <= index <= last:
            raise IndexError("Bad selection: No index '{}' in '{}'"
                             .format(index + 1, description))

        description, value = get_only_pair(menu[index])
        if isinstance(value, list):
            return self.__select(description, value, indexes, matches)
        else:
            return description, value

    def select_command(self, indexes=[], matches=[]):
        description, value = self.__select(
                self.__TOP_LEVEL_DESCRIPTION, self.__entries,
                indexes, matches)
        if not isinstance(value, str):
            raise IndexError("Expected command, but got menu '{}' instead"
                             .format(description))
        return description, value

    def __select_sub_menu(self, indexes=[], matches=[]):
        description, value = self.__select(
                self.__TOP_LEVEL_DESCRIPTION, self.__entries,
                indexes, matches)
        if not isinstance(value, list):
            raise IndexError("Expected menu, but got command '{}' instead"
                             .format(description))
        return description, value

    def add_sub_menu(self, name, indexes=[], matches=[]):
        description, menu = self.__select_sub_menu(indexes, matches)
        for entry in menu:
            if name == get_only_key(entry):
                raise IndexError("Menu already contains '{}'"
                                 .format(name))
        menu.append({ name: [] })

    def add_command(self, name, command, indexes=[], matches=[]):
        description, menu = self.__select_sub_menu(indexes, matches)
        for entry in menu:
            if name == get_only_key(entry):
                raise IndexError("Menu already contains '{}'"
                                 .format(name))
        menu.append({ name: command })
