'''Defines the Menu class
'''

from .util.dict import get_only_key, get_only_pair

class Menu(object):
    '''A class that represents a structured menu a user can choose from
       either interactively or using predefined arguments.
       The menu is a nested collection of entries.
       Every entry has a name an a value.
       A value can be either a command of type string
       or a sub-menu of type list.
    '''

    HERE = "."

    __FAKE_ROOT = {}

    def __init__(self, raw, interactive=True):
        self.__name = "root"
        self.__raw = raw
        self.__interactive = interactive
        self.__validate()

    @property
    def raw(self):
        return self.__raw

    def __validate_menu(self, name, current):
        if not isinstance(current, list):
            raise ValueError("Corrupted menu:", name)

        for entry in current:
            key, value = get_only_pair(entry)
            if isinstance(value, str):
                continue # Valid command structure

            if not isinstance(value, list):
                raise ValueError("Corrupted entry:", key)

            self.__validate_menu(key, value)

    def __validate(self):
        self.__validate_menu(self.__name, self.__raw)

    def __sub_menu_contains(self, menu, name):
        return any([name == get_only_key(entry) for entry in menu])

    def __enumerate_interactive(self, menu):
        for i, entry in enumerate(menu):
            name = get_only_key(entry)
            print("{}. {}".format(i + 1, name))

    def __select_numeric(self, name, menu, step):
        index = int(step)
        index -= 1 # Enumerated 1..N
        if not 0 <= index < len(menu):
            raise IndexError("Bad selection: No index '{}' in '{}'"
                             .format(index + 1, name))

        return index

    def __select_textual(self, name, menu, step):
        for index, entry in enumerate(menu):
            key = get_only_key(entry)
            if key.startswith(step):
                return index

        raise IndexError("Bad selection: No '{}' in '{}'"
                         .format(step, name))

    def __select_step(self, name, menu, step):
        if not step or step == self.HERE:
            return self.HERE

        if not isinstance(step, str):
            raise ValueError("Got non-string selection '{}'"
                             .format(step))

        try:
            numeric = int(step)
            return self.__select_numeric(name, menu, numeric)
        except ValueError:
            textual = step
            return self.__select_textual(name, menu, textual)

    def __select_interactive(self, name, menu):
        self.__enumerate_interactive(menu)
        print("Please select:", end=" ")
        step = input()
        return self.__select_step(name, menu, step)

    def __select_from(self, parent, current, selection):
        name, menu = get_only_pair(current)

        index = self.HERE
        if selection:
            index = self.__select_step(name, menu, selection.pop())
        elif self.__interactive:
            index = self.__select_interactive(name, menu)

        if index == self.HERE:
            return parent, current

        child = menu[index]
        child_name, child_value = get_only_pair(child)
        if isinstance(child_value, list):
            return self.__select_from(current, child, selection)
        else:
            return current, child

    def __select(self, selection):
        if not isinstance(selection, list):
            raise ValueError("Invalid selection '{}', expected a list"
                             .format(selection))

        # Selectors are appended, so we have to reverse the arguments
        # to use them as a queue (fifo), not a stack (lifo).
        selection.reverse()

        parent = self.__FAKE_ROOT
        current = { self.__name: self.__raw }
        parent, current = self.__select_from(parent, current, selection)

        # Leftover selectors are arguments, so we have to retain their
        # original order.
        selection.reverse()

        return parent, current

    def select_command(self, selection):
        _, command = self.__select(selection)
        command_name, command_value = get_only_pair(command)
        if not isinstance(command_value, str):
            raise IndexError("Expected command, but got menu '{}' instead"
                             .format(command_name))
        return command_name, command_value

    def __select_sub_menu(self, selection):
        parent, sub_menu = self.__select(selection)
        sub_menu_name, sub_menu_value = get_only_pair(sub_menu)
        if not isinstance(sub_menu_value, list):
            raise IndexError("Expected menu, but got command '{}' instead"
                             .format(name))
        return parent, sub_menu

    def __add(self, selection, name, value):
        _, sub_menu = self.__select_sub_menu(selection)
        sub_menu_name, sub_menu_value = get_only_pair(sub_menu)
        if self.__sub_menu_contains(sub_menu_value, name):
            raise ValueError("Menu already contains '{}'".format(name))
        sub_menu_value.append({ name: value })

    def add_sub_menu(self, selection, name):
        self.__add(selection, name, [])

    def add_command(self, selection, name, command):
        self.__add(selection, name, command)

    def __edit(self, selection, name, value):
        parent, entry = self.__select(selection)
        entry_name, entry_value = get_only_pair(entry)

        if value and isinstance(entry_value, list):
            raise ValueError("Cannot edit value of menu '{}'"
                             .format(entry_name))

        if name and entry_value is self.__raw:
            raise ValueError("Cannot edit name of root menu")

        parent_name, parent_value = get_only_pair(parent)
        entry_index = self.__select_textual(parent_name, parent_value, entry_name)

        new_name = name if name else entry_name
        new_value = value if value else entry_value
        parent_value[entry_index] = { new_name: new_value }

    def edit(self, selection, name=None, value=None):
        if not name and not value:
            raise ValueError("Empty edit operation aborted")

        self.__edit(selection, name, value)

    def __remove(self, selection, force):
        parent, entry = self.__select(selection)
        entry_name, entry_value = get_only_pair(entry)
        if isinstance(entry_value, list) and len(entry_value) > 0 and not force:
            raise ValueError("Menu not empty, use force to remove anyway")

        if parent is self.__FAKE_ROOT:
            self.__raw = []
            return

        parent_name, parent_value = get_only_pair(parent)
        entry_index = self.__select_textual(parent_name, parent_value, entry_name)
        del parent_value[entry_index]

    def remove(self, selection, force=False):
        self.__remove(selection, force)
