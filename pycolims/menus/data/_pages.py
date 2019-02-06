from dataclasses import dataclass as _dc
from typing import Dict as _Dict, List as _List
# from pycolims.tools.Commands import Commands
from pycolims.menus.customtypes import MentumList


@_dc
class Pages:
    """External storage of page contents"""

    _only: _List[str] = None
    _frst: _List[str] = None
    _midl: _List[str] = None
    _last: _List[str] = None

    opts: _List[str] = None

    goto_multipliers: _List[int] = None
    nav_options: MentumList = None
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

    def _generate_nav_options(self, goto_multi_list: _List[int]) -> MentumList:
        """Return a list of nav option pages, based on # of goto_possibilities"""
        if len(goto_multi_list) == 1:
            return MentumList([[' ']])
        frst_turners = ['+'],
        midl_turners = ['-', '+'],
        last_turners = ['-', ],
        return MentumList([
            ['+'],
            [['-', '+'] for x in range(1, len(goto_multi_list) - 1)],
            ['-']
        ])

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
        self.nav_options.mentum(cmd=command, return_val=False)
        self.active_turners = self.nav_options.get_active()
        self.goto_multi = self.nav_options.goto


class PageFactory:
    """Factory module to generate a Terminal object for pycolims"""
    @staticmethod
    def _return_pages_obj():
        return Pages()

    def new_pages_obj(self):
        pages_to_return = self._return_pages_obj()
        return pages_to_return
