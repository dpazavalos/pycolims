from shutil import get_terminal_size as _get_terminal_size
from dataclasses import dataclass as _dc


@_dc
class Terminal:
    """External storage of starting terminal attributes"""

    height: int = None
    width: int = None
    gap: int = None

    def set(self):
        self.height: int = _get_terminal_size()[1]
        """Terminal height, used to determine # of items that can be displayed"""
        self.gap: int = 3
        """Additional gap for term height, to accommodate space for header and nav options"""


class TermFactory:
    """Factory module to generate a Terminal object for pycolims"""
    @staticmethod
    def _return_terminal_obj():
        return Terminal()

    def new_terminal_obj(self):
        to_return = self._return_terminal_obj()
        to_return.set()
        return to_return
