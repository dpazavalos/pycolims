"""External storage of necessary page turners ('+','-')"""

from typing import List as _List
from pycolims.menus.customtypes import CrementalList


class Pages:
    """External storage of necessary page turners ('+','-'), based on terminal size.
    Stores list of possible page turners and active turners in CrementalList"""

    frst_turners = ['+'],
    midl_turners = ['-', '+'],
    last_turners = ['-', ],
    none_turners = [' ']

    opts: _List[str] = None

    goto_multipliers: _List[int] = None
    nav_options: CrementalList = None
    goto_multi: int = 0

    active_turners: _List[str] = None

    def set(self, page_options: _List[str], goto_multipliers: _List[int]):
        """Generic Set/Reset function. To be set-reset by each child menu on their runs"""

        self.goto_multi: int = 0
        """Reflection of active ndx"""

        self.opts = [cmd for cmd in page_options]
        """Navigation options for each page setup"""
        self.goto_multipliers = goto_multipliers
        """List of valid goto multipliers, based on list length and terminal height"""
        self.nav_options = self._generate_nav_options(self.goto_multipliers)
        """Cremental List of all page nav options"""
        self.active_turners = self.nav_options.get_active()

    def _generate_nav_options(self, goto_multi_list: _List[int]) -> CrementalList:
        """Return a list of nav option pages, based on # of goto_possibilities"""
        if len(goto_multi_list) == 1:
            return CrementalList(self.none_turners)

        else:
            to_crement = self.frst_turners
            for x in range(len(goto_multi_list) - 2):
                to_crement += self.midl_turners
            to_crement += self.last_turners
            return CrementalList(to_crement)

    def crement(self, key):
        """pass key to CrementalList obj holding turners, reset active_turners and multiplier"""
        self.nav_options.crement(crementer=key)
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
