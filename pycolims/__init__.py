"""Python Command Line Menu Selector (PyCoLiMS)
A command line interface single stage menu system, designed to display a given list on screen and
prompt the user to select from said list. Returns the selected item/s to the calling function in the
 same format as provided*

In the case of very large lists, PyCoLiMS breaks the list down into terminal-sized chunks with a
paging system, allowing lists larger than the screen to be processed without issue

To use, import pycolims.SelectSingle() or pycolims.SelectMulti()
once init, use .run(given_list, header="")
"""
from subprocess import call as _sp_call
from os import name as _os_name
from shutil import get_terminal_size as _get_terminal_size
from copy import deepcopy as _deepcopy
from typing import List, Dict, Tuple, Union

name = 'pycolims'


class _Menu:
    def __init__(self, given_list=None):
        self.choices: Dict[str, str] = {
            ' ': " ",
            '-': "Prev Page",
            '+': "Next Page",
            '?': "Select All",
            '!': "Clear All",
            '..': "Done"
        }
        """Possible Menu choices, with their appropriate call keys\n
        Menus generate their own call setup based on Menu type and number of values to display"""

        self.only_page: List[Tuple[str]] = [None]
        """Only nav options page when items will all fit in terminal display space\n
        (Done, plus any others)"""

        self.frst_page: List[Tuple[str]] = [None]
        """First nav options page when items extend terminal display space\n
        (Done, next page, plus any others)"""

        self.midl_page: List[Tuple[str]] = [None]
        """Middle nav options pages when items extend terminal display space\n
        (Done, prev/next page, plus any others)"""

        self.last_page: List[Tuple[str]] = [None]
        """Last nav options page when items extend terminal display space \n
        (Done, prev page, plus any others)"""

        self.given_list = given_list
        # self.menu_list: list = []
        """Menu to display. Assigned by run(). Exact type depends on menu"""

        self.term_height: int = _get_terminal_size()[1]
        """Terminal height, used to determine # of items that can be displayed"""

        self.term_gap: int = 3
        """Additional gap for term height, to accommodate space for header and nav options"""

        self.header: str = ""
        """Optional Header, assigned from each menu's run function"""

    @staticmethod
    def clear_screen() -> None:
        """Call to clear screen"""
        # subprocess.call returns the result on screen, throw it into an unused variable to hide it
        if _os_name == 'nt':
            # pylint: disable=unused-argument
            cls = _sp_call('cls', shell=True)
        else:
            # pylint: disable=unused-argument
            cls = _sp_call('clear', shell=True)

    @staticmethod
    def mentum(to_mentum: int, nav_command: str) -> int:
        """Given '+' or '-' from menus, increment or decrement by one. Used to nav pages\n
        (Name from latin root of mentum)"""
        mentums: Dict[str, str] = {'+': '__add__', '-': '__sub__'}
        # method: str = '__%s__' %
        return getattr(to_mentum, mentums[nav_command])(1)

    # Recall that indicators are stored as these strings to represent booleans
    # Display should not have to process bools
    @staticmethod
    def flip_indicator(to_flip):
        """Used to flip selection indications"""
        return '(*)' if to_flip == '( )' else '( )'

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height"""
        # When navigating, multiply entry by goto_ndx to find start
        # (If 10 options can be shown and list is 27 long,
        # then multipliers [0, 1, 2] would show 0:9, 10:19, 20:26)
        return [x for x in range(0, (len(self.given_list) // self.term_height) + 1)]

    def generate_nav_options(self, goto_multi_list: List[int]) -> List[List[Tuple[str]]]:
        """Return a list of nav option pages, based on # of goto_possibilities"""
        if len(goto_multi_list) == 1:
            return [self.only_page]
        return [self.frst_page] +\
               [self.midl_page for x in range(1, len(goto_multi_list)-1)] + \
               [self.last_page]

    def valid_navigator(self, nav_command: str) -> bool:
        """Check if a char is a valid nav command"""
        return nav_command in [x for x in self.choices]

    # menu options should be [original index, Item/List itself]  ( ['7', '[Entry Val]'] )
    # nav options should be [nav control, nav descriptor]   ( ['+', 'Next Page'] )
    # inlist items can be a single item or nested list, items will be printed as joined string
    def displayer(self, inlist: List[List[str]], navopts: List[Tuple[str]]) -> str:
        """Called by a Navigator function, displays a given list on screen, along with nav options\n
        Selected option must be one shown on screen"""
        to_display: List[Union[List, Tuple]] = []       # ["0", "a"], ["+", "Next Page"]
        valid_selections: List[str] = []                # String'd int entries for menu Values

        # indexes of items passed through arg inlist
        for item in inlist:
            to_display.append(item)
            valid_selections.append(str(item[0]))

        # Given Navigation options
        for opt in navopts:
            to_display.append(opt)
            if opt[0] != " ":
                valid_selections.append(str(opt[0]))

        prompt: str = ''
        while prompt not in valid_selections:
            print(self.header)
            for each in to_display:
                print(
                    f'({each[0]})'.rjust(5), ' '.join([str(each[x]) for x in range(1, len(each))])
                )
            prompt = input()
            self.clear_screen()
        return prompt

    def handle_given_list(self, to_handle: Union[list, tuple, dict]):
        """Prepare menu_in for proper sorting, based on type"""
        if isinstance(to_handle, dict):
            self.given_list = [key for key in to_handle.keys()]
        elif isinstance(to_handle, list):
            self.given_list = _deepcopy(to_handle)
        elif isinstance(to_handle, tuple):
            self.given_list = list(to_handle)

    def gen_nav_pages(self,
                      only_choices: List[str], frst_choices: List[str],
                      midl_choices: List[str], last_choices: List[str]) -> None:
        """Creates Navigation pages, each pulling entries from self.choices\n
        """
        self.only_page = [(x, self.choices[x]) for x in only_choices]
        self.frst_page = [(x, self.choices[x]) for x in frst_choices]
        self.midl_page = [(x, self.choices[x]) for x in midl_choices]
        self.last_page = [(x, self.choices[x]) for x in last_choices]
        self.term_height -= len(self.only_page) + self.term_gap

    def navigator(self) -> list:
        """Function to handle handoff of menu_in items to displayer\n
        This function must be rewritten for each menu type"""

    def run(self, given_list: Union[List[any],
                                    List[Tuple[bool, any]],
                                    Tuple[any],
                                    Dict[any, any]],
            header: str = "") -> Union[any,
                                       List[any],
                                       List[Tuple[bool, any]]]:
        """Given a list, prompt for selection of item or items in a list.\n
        Returns a list with nested booleans indicating if selected or not\n
        [item for [boolean, item] in menu.run(menu_in) if boolean]"""
        # self.menu_list = deepcopy(menu_in)
        self.handle_given_list(given_list)
        self.header = header
        return self.navigator()


class SelectSingle(_Menu):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n
    List can be flat or an array\n\n
    Once init, call run()"""

    def navigator(self):
        """Select Single Navigator
        Sizes list according to term height, navigates pages, returns a single selection"""

        self.gen_nav_pages(only_choices=[' ', ' '],
                           frst_choices=[' ', '+'],
                           midl_choices=['-', '+'],
                           last_choices=['-', ' '])

        # Modify self.menu_list, inserting index [orig_ndx, *desired_item(s)]
        for ndx in range(len(self.given_list)):
            try:
                # inserting index number at beginning of nested list
                self.given_list[ndx].insert(0, ndx)
            except AttributeError:
                # item is not a list. Turn to list with index at beginning
                self.given_list[ndx] = [ndx, self.given_list[ndx]]
            except KeyError:
                print(type(self.given_list))
                print(self.given_list)
                exit(1)

        goto_multipliers: List[int] = self.generate_goto_multipliers()
        nav_options: List[List[Tuple[str]]] = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0
        """Multiply by self.term_height to determine starting index"""

        self.clear_screen()
        while True:
            disp_start: int = goto_multi * self.term_height

            command = self.displayer(self.given_list[disp_start: (disp_start + self.term_height)],
                                     nav_options[goto_multi])
            """Command is the returned str from displayer (nav option or a single menu selection)"""

            if not self.valid_navigator(command):
                selected_val = self.given_list[int(command)][1::]
                """Selection pulled from menu_list, based on command. Value to be returned"""
                break

            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.mentum(goto_multi, command)
                except (KeyError, IndexError):
                    # Key and Index errors cover the possible "Next page when last page"
                    pass

        return selected_val[0] if len(selected_val) == 1 else selected_val


class SelectMulti(_Menu):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n
    Once init, call run()"""

    def navigator(self) -> list:
        """Select Multiple Navigator
        Sizes list according to term height, navigates pages,
        flips ( ) indicator based off displayer's return value"""

        self.gen_nav_pages(only_choices=[' ', ' ', '?', '!', '..'],
                           frst_choices=[' ', '+', '?', '!', '..'],
                           midl_choices=['-', '+', '?', '!', '..'],
                           last_choices=['-', ' ', '?', '!', '..'])

        # Modify self.menu_list, preserving index [orig_ndx, *desired_item(s)]
        for ndx in range(len(self.given_list)):
            if isinstance(self.given_list[ndx], list):
                if isinstance(self.given_list[ndx][0], bool):
                    # True/False bool flags are converted here to visual indicators,
                    # and returned to bools by end of run, allowing consistent passing to
                    # self.displayer, without nested checks needed
                    ind = '(*)' if self.given_list[ndx][0] else '( )'
                    self.given_list[ndx] = [ndx, ind, self.given_list[ndx][1]]
            else:
                self.given_list[ndx] = [ndx, '( )', self.given_list[ndx]]

        goto_multipliers = self.generate_goto_multipliers()
        nav_options = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0  # Multiply by self.term_height to determine starting index
        command = ""
        '''Command is the returned str from displayer, either a nav option or an item to trigger'''

        # Call Displayer to determine necessary selection(s)
        self.clear_screen()
        while command != "..":
            disp_start = goto_multi * self.term_height
            command = self.displayer(self.given_list[disp_start: disp_start + self.term_height],
                                     nav_options[goto_multi])

            # Try 'doing' the returned value (by index integer)
            if not self.valid_navigator(command):
                # Execute based on selection
                self.given_list[int(command)][1] = \
                    self.flip_indicator(self.given_list[int(command)][1])

            # Select All
            if command == '?':
                for entry in self.given_list:
                    entry[1] = '(*)'

            # Clear All
            if command == '!':
                for entry in self.given_list:
                    entry[1] = '( )'

            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.mentum(goto_multi, command)
                except KeyError:
                    pass

        return [
            [(x[1] == '(*)')] + x[2::]
            for x in self.given_list
        ]  # recall that x[0] was our index, Not needed.
