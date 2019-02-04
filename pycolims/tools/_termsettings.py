from shutil import get_terminal_size as _get_terminal_size
from dataclasses import dataclass as _dc


@_dc
class Terminal:
    term_height: int = _get_terminal_size()[1]
    """Terminal height, used to determine # of items that can be displayed"""

    term_gap: int = 3
    """Additional gap for term height, to accommodate space for header and nav options"""
