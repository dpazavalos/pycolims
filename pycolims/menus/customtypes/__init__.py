from pycolims.menus.customtypes import _cremental_list


class CrementalList(_cremental_list.CrementalList):
    """Extension of default list obj. Adds a tracking index for an 'active' item

get_active() -> any:
    Returns item from list using active ndx

set_ndx(new_ndx: int) -> None
    Attempts to set active ndx.
    Raises a Value Error if given ndx is outside list ndx

crement(cmd: str, return_value=False) -> Optional[int]:
    Attempts to increment or decrement
"""
