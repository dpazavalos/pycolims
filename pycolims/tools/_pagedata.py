from dataclasses import dataclass as _dc
from typing import Dict as _Dict, _List as _List, _Tuple as _Tuple
#
@_dc
class Pages:
    choices: _Dict[str, str] = {
        ' ': " ",
        '-': "Prev Page",
        '+': "Next Page",
        '?': "Select All",
        '!': "Clear All",
        '..': "Done"
    }
    """Possible Menu choices, with their appropriate call keys\n
    Menus generate their own call setup based on Menu type and number of values to display"""

    only_page: _List[_Tuple[str]] = [None]
    """Only nav options page when items will all fit in terminal display space\n
    (Done, plus any others)"""

    frst_page: _List[_Tuple[str]] = [None]
    """First nav options page when items extend terminal display space\n
    (Done, next page, plus any others)"""

    midl_page: _List[_Tuple[str]] = [None]
    """Middle nav options pages when items extend terminal display space\n
    (Done, prev/next page, plus any others)"""

    last_page: _List[_Tuple[str]] = [None]
    """Last nav options page when items extend terminal display space \n
    (Done, prev page, plus any others)"""

    def reset(self):