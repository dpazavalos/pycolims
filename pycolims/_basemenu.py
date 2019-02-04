"""Python Command Line Menu Selector (PyCoLiMS)
A command line interface single stage menu system, designed to display a given list on screen and
prompt the user to select from said list. Returns the selected item/s to the calling function in the
 same format as provided*

In the case of very large lists, PyCoLiMS breaks the list down into terminal-sized chunks with a
paging system, allowing lists larger than the screen to be processed without issue

To use, import pycolims.SelectSingle() or pycolims.SelectMulti()
once init, use .run(given_list, header="")
"""

from copy import deepcopy as _deepcopy
from typing import List, Dict, Tuple, Union
from pycolims.tools import Factory


class _Menu:
    def __init__(self, given_list=None):

        self.given_list = given_list
        # self.menu_list: list = []
        """Menu to display. Assigned by run(). Exact type depends on menu"""

        self.header: str = ""
        """Optional Header, assigned from each menu's run function"""

        self.term: Factory.Terminal = Factory.build.new_terminal_obj()

        self.page: Factory.Pages = Factory.build.new_pages_obj()

        self.statics: Factory.Statics = Factory.build.new_statics_obj()

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height"""
        # if 27 options but only 10 can be shown, then multipliers [0, 1, 2] for 0:9, 10:19, 20:26
        return [x for x in range(0, ((len(self.given_list) // self.term.height) + 1))]

    def generate_nav_options(self, goto_multi_list: List[int]) -> List[List[Tuple[str]]]:
        """Return a list of nav option pages, based on # of goto_possibilities"""
        if len(goto_multi_list) == 1:
            return [self.page.only]
        return [self.page.frst] + \
               [self.page.midl for x in range(1, len(goto_multi_list ) -1)] + \
               [self.page.last]

    def valid_navigator(self, nav_command: str) -> bool:
        """Check if a char is a valid nav command"""
        return (nav_command in self.page.cmd_turners) or (nav_command in self.page.cmd_options)

    # menu options should be [original index, Item/List itself]  ( ['7', '[Entry Val]'] )
    # nav options should be [nav control, nav descriptor]   ( ['+', 'Next Page'] )
    # inlist items can be a single item or nested list, items will be printed as joined string
    def displayer(self, inlist: List[List[str]],
                  turners, options,
                  navopts: List[Tuple[str]]) -> str:
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

    def gen_page_turners(self,
                         only_choices: List[str], frst_choices: List[str],
                         midl_choices: List[str], last_choices: List[str]) -> None:
        """Creates Navigation pages, each pulling entries from self.choices\n
        """
        self.page.only = [(x, self.choices[x]) for x in only_choices]
        self.page.frst = [(x, self.choices[x]) for x in frst_choices]
        self.page.midl = [(x, self.choices[x]) for x in midl_choices]
        self.page.last = [(x, self.choices[x]) for x in last_choices]

    def gen_page_options(self, **nav_opts: str):
        print(self.page.cmd_options)
        pass


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





