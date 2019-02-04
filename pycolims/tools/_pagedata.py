from dataclasses import dataclass as _dc
from typing import Dict as _Dict, List as _List, Tuple as _Tuple
from pycolims.tools.Commands import DisplayCmd


@_dc
class Pages:
    """External storage of page contents"""

    only: _List[_List[str]]
    frst: _List[_List[str]]
    midl: _List[_List[str]]
    last: _List[_List[str]]

    opts: _List[_List[str]]

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

    def reset(self,
              only_turners: _List[str], frst_turners: _List[str],
              midl_turners: _List[str], last_turners: _List[str],
              page_options: _List[str]):
        """Generic Set/Reset function. To be usd by each child menu as needed"""

        self.only = self._validate_cmds(only_turners, DisplayCmd.turners)
        """Page Turners when items will all fit in terminal display space"""

        self.frst = self._validate_cmds(frst_turners, DisplayCmd.turners)
        """First page Turners when items extend terminal display space"""

        self.midl = self._validate_cmds(midl_turners, DisplayCmd.turners)
        """Middle pages Turners when items extend terminal display space"""

        self.last = self._validate_cmds(last_turners, DisplayCmd.turners)
        """Last page turners when items extend terminal display space"""

        self.opts = self._validate_cmds(page_options, DisplayCmd.options)
        """Navigation options for each page setup"""


class PageFactory:
    """Factory module to generate a Terminal object for pycolims"""
    @staticmethod
    def _return_pages_obj():
        return Pages()

    def new_pages_obj(self):
        pages_to_return = self._return_pages_obj()
        return pages_to_return
