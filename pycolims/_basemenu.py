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
from pycolims.tools.Commands import DisplayCmd


class _Menu:
    def __init__(self):

        self.given_list = None
        """Menu to break and display"""

        self.header: str = ""
        """Optional Header, assigned from each menu's run function"""

        self.term: Factory.Terminal = Factory.build.new_terminal_obj()

        self.page: Factory.Pages = Factory.build.new_pages_obj()

        self.command_check = DisplayCmd()

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height\n
        Used to configure page data"""
        # if 27 options but only 10 can be shown, then multipliers [0, 1, 2] for 0:9, 10:19, 20:26
        return [x for x in range(0, ((len(self.given_list) // self.term.height) + 1))]

    def valid_option(self, nav_command: str) -> bool:
        """Check if an option is a valid bottom row option (NOT page turners!)"""
        return nav_command in self.page.opts

    def displayer(self, itemlist: List[List[str]],
                  turners: List[str]) -> str:
        """Called by a Navigator function, displays a given list on screen, along with nav options\n
        Selected option must be one shown on screen"""
        to_display: List[Union[List, Tuple]] = []       # ["0", "a"], items to display
        current_turners: List[str] = []
        valid_selections: List[str] = []                # String'd int entries for menu Values

        for item in itemlist:
            to_display.append(item)
            valid_selections.append(str(item[0]))       # ["0", "a"]

        for turner in turners:
            current_turners.append(turner)
            if turner != " ":
                valid_selections.append(turner)

        # Add keys from activated page opts
        for opt in self.page.opts:
            valid_selections.append(opt)

        prompt: str = ''
        while prompt not in valid_selections:
            self.term.clear()
            print(self.header)
            for item in to_display:
                print(self.display_line(item))
            for turner in current_turners:
                print(self.display_line([turner, self.command_check.turners[turners]]))
            for opt in self.page.opts:
                print(self.option_line(opt), end=' ')

            try:
                prompt = input()
            except KeyboardInterrupt:
                prompt = self.command_check.options_inv["Break"]
        return prompt

    def display_line(self, to_display: Union[List, Tuple]) -> str:
        """creates a display line for displayer. Modified by menu types"""

    def option_line(self, option: str) -> str:
        """creates an option line for displayer"""
        return ' '.join((f'{option}'.rjust(5),
                         self.command_check.options[option]))

    def retype_given_list(self, to_handle: Union[list, tuple, dict]):
        """Prepare menu_in into proper type """
        if isinstance(to_handle, dict):
            self.given_list = [key for key in to_handle.keys()]
        elif isinstance(to_handle, list):
            self.given_list = _deepcopy(to_handle)
        elif isinstance(to_handle, tuple):
            self.given_list = list(to_handle)

    def command_handler(self, command: str):
        """responsible for managing commands given back to navigator"""

    def _cmd_break(self):
        """Common command"""
        raise KeyboardInterrupt

    def navigator(self) -> list:
        """Function to handle handoff of menu_in items to displayer\n
        This function is rewritten for each menu type"""

    def run(self,
            given_list: Union[List[any],
                              List[Tuple[bool, any]],
                              Tuple[any],
                              Dict[any, any]],
            header: str = "") -> Union[any,
                                       List[any],
                                       List[Tuple[bool, any]]]:
        """Given a list, prompt for selection of item or items in a list.\n
        Returns a list with nested booleans indicating if selected or not\n
        [item for [boolean, item] in menu.run(menu_in) if boolean]"""
        self.retype_given_list(given_list)
        self.header = header
        return self.navigator()
