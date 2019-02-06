"""Template class for base menu. Used by factory and side loaded menu objects that require knowledge
of menu functions"""

from typing import List, Dict, Tuple, Union
from pycolims.data import _data_zFactory as DataFactory
from copy import deepcopy as _deepcopy
from pycolims.data._base_menu_template import MenuTemplate


class MenuEngine(MenuTemplate):
    """Template with set functions to build menus"""

    term: DataFactory.Terminal
    page: DataFactory.Pages
    command: DataFactory.Command
    work: DataFactory.Work
    _handler: dict = None

    def set(self, list_to_give=None, header=None):

        self.command: DataFactory.Command = DataFactory.build.new_command_obj()
        self.term: DataFactory.Terminal = DataFactory.build.new_terminal_obj()
        self.page: DataFactory.Pages = DataFactory.build.new_pages_obj()
        if None not in [list_to_give, header]
        self.work: DataFactory.Work = DataFactory.build.new_work_obj()

        self._handler = {
            self.command.turners_inv["Prev Page"]: self._cmd_mentum_d,
            self.command.turners_inv["Next Page"]: self._cmd_mentum_i,
            self.command.options_inv["Select All"]: self._cmd_sel,
            self.command.options_inv["Clear All"]: self._cmd_clr,
            self.command.options_inv["Returned Selected"]: self._cmd_clr,
            self.command.options_inv["Break"]: self._cmd_break,
        }

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height\n
        Used to configure page data"""
        # if 27 options but only 10 can be shown, then multipliers [0, 1, 2] for 0:9, 10:19, 20:26
        return [x for x in range(0, ((len(self.given_list) // self.term.height) + 1))]

    def displayer(self, itemlist: List[List[str]]) -> str:
        """Called by a Navigator function, displays a given list on screen, along with nav options\n
        Selected option must be one shown on screen"""
        to_display: List[Union[List, Tuple]] = []       # ["0", "a"], items to display
        current_turners: List[str] = []
        valid_selections: List[str] = []                # String'd int entries for menu Values

        for item in itemlist:
            to_display.append(item)
            valid_selections.append(str(item[0]))       # ["0", "a"]

        for turner in self.page.active_turners:
            current_turners.append(turner)
            if turner != " ":
                valid_selections.append(turner)

        for opt in self.page.opts:
            valid_selections.append(opt)

        prompt: str = ''
        while prompt not in valid_selections:
            self.term.clear()
            print(self.header)
            for item in to_display:
                print(self.display_line(item))
            for turner in current_turners:
                print(self.display_line([turner, self.command.turners[turner]]))
            for opt in self.page.opts:
                print(self.option_line(opt), end=' ')

            try:
                prompt = input()
            except KeyboardInterrupt:
                prompt = self.command.options_inv["Break"]
        self.term.clear()
        return prompt

    def display_line(self, to_display: Union[List, Tuple]) -> str:
        """creates a display line for displayer. Modified by menu types"""

    def option_line(self, option: str) -> str:
        """creates an option line for displayer"""
        return ' '.join((f'({option})'.rjust(5),
                         self.command.options[option]))

    def retype_given_list(self, to_handle: Union[list, tuple, dict]):
        """Prepare menu_in into proper type """
        if isinstance(to_handle, dict):
            self.given_list = [key for key in to_handle.keys()]
        elif isinstance(to_handle, list):
            self.given_list = _deepcopy(to_handle)
        elif isinstance(to_handle, tuple):
            self.given_list = list(to_handle)

    def handler(self, command: str):
        self._handler[command]()

    def _cmd_mentum_d(self):
        """Mentum increment command caller"""
        self.page.mentum('-')

    def _cmd_mentum_i(self):
        """Mentum increment command caller"""
        self.page.mentum('+')

    def _cmd_sel(self):
        """Set all booleans to True"""
        for given in self.given_list:
            given[1] = True

    def _cmd_clr(self):
        """Set all booleans to True"""
        for given in self.given_list:
            given[1] = False

    def _cmd_ret(self):
        """Close repeating flag"""
        self.repeating = False

    def _cmd_break(self):
        """Common interrupt command"""
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
