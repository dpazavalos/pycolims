"""Template class for base menu. Used by factory and side loaded menu objects that require knowledge
of menu functions"""

from typing import List, Dict, Tuple, Union
from pycolims.menus.data import *


class MenuEngine:
    """Template with set functions to build menus"""

    def __init__(self):

        self.term = DataTerminal()
        self.page = DataPages()
        self.command = DataCommands()
        self.work = DataInput()

        self._handler = {
            self.command.turners_inv["Prev Page"]: self._cmd_page_dec,
            self.command.turners_inv["Next Page"]: self._cmd_page_inc,
            self.command.options_inv["Select All"]: self._cmd_sel,
            self.command.options_inv["Clear All"]: self._cmd_clr,
            self.command.options_inv["Flip All"]: self._cmd_flip,
            self.command.options_inv["Return Selected"]: self._cmd_ret,
            self.command.options_inv["Break"]: self._cmd_break,
        }
        """Handler for command keys. Used to access command functions"""

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height
        Used to configure page data"""
        # if 27 options but only 10 can be shown,
        #  then multipliers [0, 1, 2] for 0:9, 10:19, 20:26
        return [x for x in range(0, ((len(self.work.given_list) // self.term.height) + 1))]

    def displayer(self, itemlist: List[List[str]]) -> str:
        """Called by a Navigator function, displays a given list on screen,
        along with nav options. Selected option must be one shown on screen"""
        to_display: List[Union[List, Tuple]] = []       # ["0", "a"], items to display
        valid_selections: List[str] = []                # String'd int entries for menu Values

        for item in itemlist:
            to_display.append(item)
            valid_selections.append(str(item[0]))       # ["0", "a"]

        for turner in self.page.active_turners:
            if turner != " ":
                valid_selections.append(turner)

        for opt in self.page.opts:
            valid_selections.append(opt)

        prompt: str = 'none'
        while prompt not in valid_selections:
            self.term.clear()

            print(self.work.header)
            self.display_line(to_display)
            self.display_turners()
            self.display_opts()
            print()

            try:
                prompt = input()
            except KeyboardInterrupt:
                prompt = self.command.options_inv["Break"]

        return prompt

    def display_line(self, to_display: List[List[any]]):
        """Generic function for item line display. Inherited by
        child obj"""

    def display_turners(self):
        """Display active page turners in separate lines"""
        for turn in self.page.active_turners:
            print(f'({turn})'.rjust(5), self.command.turners[turn])

    def display_opts(self):
        """Display active options at bottom row"""
        for opt in self.page.opts:
            print(f'({opt})'.rjust(5), self.command.options[opt], end='')

    def option_line(self, option: str) -> str:
        """creates an option line for displayer"""
        return ' '.join((f'({option})'.rjust(5),
                         self.command.options[option]))

    def command_handler(self, command: str):
        self._handler[command]()

    def _cmd_page_dec(self):
        """Send crement decreaser to page, to then send to listcrement obj"""
        self.page.crement('-')

    def _cmd_page_inc(self):
        """Send crement increaser to page, to then send to listcrement obj"""
        self.page.crement('+')

    def _cmd_sel(self):
        """Set all booleans to True"""
        for given in self.work.given_list:
            given[1] = True

    def _cmd_clr(self):
        """Set all booleans to True"""
        for given in self.work.given_list:
            given[1] = False

    def _cmd_flip(self):
        """Set all booleans to True"""
        for given in self.work.given_list:
            given[1] = not given[1]

    def _cmd_ret(self):
        """Close repeating flag"""
        self.work.repeating = False

    def _cmd_break(self):
        """Common interrupt command"""
        raise KeyboardInterrupt("Manually interrupted")

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

        # Set work storage modules with new info
        self.work.set(given_list, header)
        # Set terminal info to most recent status
        self.term.set()

        return self.navigator()
