name = 'pycolims'
from shutil import get_terminal_size
from copy import deepcopy
from typing import List, Dict, Tuple, Union


class _Menu(object):
    def __init__(self, choices=None, only_page=None, frst_page=None, midl_page=None, last_page=None, header=None,
                 term_height=None, term_gap=None, menu_list=None):
        self.choices = choices
        self.choices: List[Tuple[str]] = [(" ", " "),
                                          ("-", "Prev Page"),
                                          ("+", "Next Page"),
                                          ("!", "Clear All"),
                                          ("..", "Done")]
        """Possible Menu choices, with their appropriate call keys as ndx 0\n
        Each menu generates their own menu call setup based on Menu type and number of values to display"""

        self.only_page = only_page
        self.only_page: List[Tuple[str]] = [None]
        """Only nav options page when items will all fit in terminal display space (Done, plus any others)"""

        self.frst_page = frst_page
        self.frst_page: List[Tuple[str]] = [None]
        """First nav options page when items extend terminal display space (Done, next page, plus any others)"""

        self.midl_page = midl_page
        self.midl_page: List[Tuple[str]] = [None]
        """Middle nav options pages when items extend terminal display space (Done, prev/next page, plus any others)"""

        self.last_page = last_page
        self.last_page: List[Tuple[str]] = [None]
        """Last nav options page when items extend terminal display space (Done, prev page, plus any others)"""

        self.menu_list = menu_list
        # self.menu_list: list = []
        """Menu to display. Assigned by run(). Exact type depends on menu"""

        self.term_height = term_height
        self.term_height: int = get_terminal_size()[1]
        """Terminal height, used to determine # of items that can be displayed\n
        Menus may adjust size as needed"""

        self.term_gap = term_gap
        self.term_gap: int = 3
        """Additional gap for term height, to accommodate space for header and nav options"""

        self.header = header
        self.header: str = ""
        """Optional Header, assigned from each menu's run function"""

    def clear_screen(self) -> None:
        """Clears screen, based off term_height"""
        print("\n" * (self.term_height*2))

    @staticmethod
    def mentum(x: int, nav_command: str) -> int:
        """Given '+' or '-', increment or decrement by one (Name from latin root of mentum). Used to nav page views"""
        mentums: Dict[str, str] = {'+': '__add__', '-': '__sub__'}
        # method: str = '__%s__' %
        return getattr(x, mentums[nav_command])(1)

    # Recall that indicators are stored as these strings to represent booleans. Display should not have to process bools
    @staticmethod
    def flip_indicator(to_flip):
        """Used to flip selection indications"""
        return '(*)' if to_flip == '( )' else '( )'

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height"""
        # When navigating, multiply entry by goto_ndx to find start
        # (If 10 options can be shown and list is 27 long, then multipliers [0, 1, 2] would show 0:9, 10:19, 20:26)
        return [x for x in range(0, (len(self.menu_list) // self.term_height) + 1)]

    def generate_nav_options(self, goto_multi_list: List[int]) -> List[List[Tuple[str]]]:
        """Return a list of nav option pages, based on # of goto_possibilities"""
        if len(goto_multi_list) == 1:
            return [self.only_page]
        else:
            return [self.frst_page] + [self.midl_page for x in range(1, len(goto_multi_list)-1)] + [self.last_page]

    def valid_navigator(self, nav_command: str) -> bool:
        """Check if a char is a valid nav command"""
        return nav_command in [x[0] for x in self.choices]

    # menu options should be [original index, Item/List itself]  ( ['7', '[Entry Val]'] )
    # nav options should be [nav control, nav descriptor]   ( ['+', 'Next Page'] )
    # inlist items can be a single item or nested list, items will be printed as joined string
    def displayer(self, inlist: List[List[str]], navopts: List[Tuple[str]]) -> str:
        """Called by a Menu Navigator function, displays a given list on screen, along with nav options\n
        Selected option must be one shown on screen"""
        to_display: List[Union[List, Tuple]] = []       # ["0", "a"], ["+", "Next Page"]
        valid_selections: List[str] = []                # String'd int entries for menu Values

        # indexes of items passed through arg inlist
        for x in inlist:
            to_display.append(x)
            valid_selections.append(str(x[0]))

        # Given Navigation options
        for opt in navopts:
            to_display.append(opt)
            if opt[0] is not " ":
                valid_selections.append(str(opt[0]))

        prompt: str = ''
        while prompt not in valid_selections:
            print(self.header)
            for each in to_display:
                print(f'({each[0]})'.rjust(5), ' '.join([str(each[x]) for x in range(1, len(each))]))
            prompt = input()
            self.clear_screen()
        return prompt

    def handle_menu_in(self, menu_in: Union[list, tuple, dict]):
        """Prepare menu_in for proper sorting, based on type"""
        if type(menu_in) == dict:
            self.menu_list = [key for key in menu_in.keys()]
        elif type(menu_in) == list:
            self.menu_list = deepcopy(menu_in)
        elif type(menu_in) == tuple:
            self.menu_list = list(menu_in)

    def gen_nav_pages(self, only_choices: List[int], frst_choices: List[int], midl_choices: List[int],
                      last_choices: List[int]) -> None:
        """Creates Navigation pages, each pulling entries from self.choices\n
        """
        self.only_page = [self.choices[x] for x in only_choices]
        self.frst_page = [self.choices[x] for x in frst_choices]
        self.midl_page = [self.choices[x] for x in midl_choices]
        self.last_page = [self.choices[x] for x in last_choices]
        self.term_height -= len(self.only_page) + self.term_gap

    def navigator(self) -> list:
        """Function to handle handoff of menu_in items to displayer\n
        This function must be rewritten for each menu type"""
        pass

    def run(self, array_in: Union[List[any],
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
        self.handle_menu_in(array_in)
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

        self.gen_nav_pages(only_choices=[0, 0],
                           frst_choices=[0, 2],
                           midl_choices=[1, 2],
                           last_choices=[1, 0])

        # Modify self.menu_list, inserting index [orig_ndx, *desired_item(s)]
        for ndx in range(len(self.menu_list)):
            try:
                # inserting index number at beginning of nested list
                self.menu_list[ndx].insert(0, ndx)
            except AttributeError:
                # item is not a list. Turn to list with index at beginning
                self.menu_list[ndx] = [ndx, self.menu_list[ndx]]
            except KeyError:
                print(type(self.menu_list))
                print(self.menu_list)
                exit(1)

        goto_multipliers: List[int] = self.generate_goto_multipliers()
        nav_options: List[List[Tuple[str]]] = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0
        """Multiply by self.term_height to determine starting index"""
        command: str = ''
        """Command is the returned str from displayer, either a nav option or a single menu selection"""
        selected_val = None
        """Selection pulled from menu_list, based on command. Value to be returned"""

        self.clear_screen()
        while True:
            disp_start: int = goto_multi * self.term_height
            command = self.displayer(self.menu_list[disp_start:(disp_start + self.term_height)],
                                     nav_options[goto_multi])

            if not self.valid_navigator(command):
                selected_val = self.menu_list[int(command)][1::]
                break

            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.mentum(goto_multi, command)
                except (KeyError, IndexError):
                    # Key and Index errors cover the possible "Next page when last page" or
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

        self.gen_nav_pages(only_choices=[0, 0, 3, 4],
                           frst_choices=[0, 2, 3, 4],
                           midl_choices=[1, 2, 3, 4],
                           last_choices=[1, 0, 3, 4])

        # Modify self.menu_list, preserving index [orig_ndx, *desired_item(s)]
        for ndx in range(len(self.menu_list)):
            if type(self.menu_list[ndx]) == list:
                if type(self.menu_list[ndx][0]) == bool:
                    # True/False bool flags are converted here to visual indicators, and returned to bools by end of run
                    # This allows consistent passing to self.displayer, without nested checks needed
                    ind = '(*)' if self.menu_list[ndx][0] else '( )'
                    self.menu_list[ndx] = [ndx, ind, self.menu_list[ndx][1]]
            else:
                self.menu_list[ndx] = [ndx, '( )', self.menu_list[ndx]]

        goto_multipliers = self.generate_goto_multipliers()
        nav_options = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0  # Multiply by self.term_height to determine starting index
        command = ""
        """Command is the returned str from displayer, either a nav option or a multi menu item to trigger"""

        # Call Displayer to determine necessary selection(s)
        self.clear_screen()
        while command != "..":
            disp_start = goto_multi * self.term_height
            command = self.displayer(self.menu_list[disp_start:disp_start + self.term_height], nav_options[goto_multi])

            # Try 'doing' the returned value (by index integer)
            if not self.valid_navigator(command):
                # Execute based on selection
                self.menu_list[int(command)][1] = self.flip_indicator(self.menu_list[int(command)][1])
            if command is '!':
                for entry in self.menu_list:
                    entry[1] = '( )'
            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.mentum(goto_multi, command)
                except KeyError:
                    pass

        return [[(x[1] == '(*)')] + x[2::]
                for x in self.menu_list]  # recall that x[0] was our index, Not needed.


