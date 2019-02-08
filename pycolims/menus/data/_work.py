"""Separate SubObject for menus, to hold working data"""
from copy import deepcopy as _deepcopy
from typing import Union as _Union


class Work:
    given_list = None
    repeating = None
    header: str = None

    def set(self, list_to_give, header):
        """Prepare working data for processing"""

        self.given_list = self.retype_given_list(list_to_give)
        """Menu to break and display"""

        self.header: str = header
        """Optional Header, assigned from each menu's run function"""

        self.repeating = True
        """Repeating flag used keep navigators open"""

    @staticmethod
    def retype_given_list(to_handle: _Union[list, tuple, dict]) -> list:
        """Prepare menu_in into proper type """
        if isinstance(to_handle, dict):
            return [key for key in to_handle.keys()]
        elif isinstance(to_handle, list):
            return _deepcopy(to_handle)
        elif isinstance(to_handle, tuple):
            return list(to_handle)


class WorkFactory:
    """Factory module to generate a Command obj for Pycolims"""

    @staticmethod
    def _return_work_obj():
        return Work()

    def new_work_obj(self):
        to_return = self._return_work_obj()
        return to_return
