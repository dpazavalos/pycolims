from dataclasses import dataclass as _dc
from typing import Dict as _Dict, List as _List
# from pycolims.tools.Commands import Commands
from pycolims.menus.customtypes import ListCrement


@_dc
class Pages:
    """External storage of page contents"""

    frst_turners = ['+'],
    midl_turners = ['-', '+'],
    last_turners = ['-', ],

    opts: _List[str] = None

    goto_multipliers: _List[int] = None
    nav_options: ListCrement = None
    goto_multi: int = 0

    active_turners: _List[str] = None

    def set(self,
            page_options: _List[str],
            goto_multipliers: _List[int]):
        """Generic Set/Reset function. To be usd by each child menu as needed"""

        # self._only = self._validate_cmds(only_turners, Commands.turners)
        """Page Turners when items will all fit in terminal display space"""
        # self._frst = [turner for turner in frst_turners]
        """First page Turners when items extend terminal display space"""
        # self._midl = [turner for turner in midl_turners]
        """Middle pages Turners when items extend terminal display space"""
        # self._last = [turner for turner in last_turners]
        """Last page turners when items extend terminal display space"""
        self.opts = [cmd for cmd in page_options]
        """Navigation options for each page setup"""

        self.goto_multipliers = goto_multipliers
        """List of valid goto multipliers, based on list length and terminal height"""
        self.nav_options = self._generate_nav_options(self.goto_multipliers)
        """Mentum List of all page nav options"""
        self.active_turners = self.nav_options.get_active()

    def _generate_nav_options(self, goto_multi_list: _List[int]) -> ListCrement:
        """Return a list of nav option pages, based on # of goto_possibilities"""
        if len(goto_multi_list) == 1:
            return ListCrement(self.frst_turners)

        else:
            to_crement = self.frst_turners
            for x in range(len(goto_multi_list) - 2):
                to_crement += self.midl_turners
            to_crement += self.last_turners
            return ListCrement(to_crement)

    def is_valid_navigator(self, nav_command: str) -> bool:
        """Check if a char is a valid nav command"""
        return nav_command in self.opts

    @ staticmethod
    def _validate_cmds(cmds: _List[str], valid_commands: _Dict[str, str]) -> _List[_List[str]]:
        """Checks page cmd keys against valid_commands list, returns in nested list with cmd names
        Raises specific value error if not in"""
        to_return = []
        for c in cmds:
            if c not in valid_commands:
                raise ValueError(f"{c} is not in {valid_commands}!")
            to_return.append(c)
        return [[cmd, valid_commands[cmd]] for cmd in to_return]

    def mentum(self, command):
        self.nav_options.crement(crementer=command)
        self.active_turners = self.nav_options.get_active()
        self.goto_multi = self.nav_options.ndx


class PageFactory:
    """Factory module to generate a Terminal object for pycolims"""
    @staticmethod
    def _return_pages_obj():
        return Pages()

    def new_pages_obj(self):
        pages_to_return = self._return_pages_obj()
        return pages_to_return
