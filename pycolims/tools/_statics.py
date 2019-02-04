from subprocess import call as _sp_call
from os import name as _os_name


class Statics:
    """External storage of non class specific tools"""

    @staticmethod
    def clear_screen() -> None:
        """Call to clear screen"""
        if _os_name == 'nt':
            _sp_call('cls', shell=True)
        else:
            _sp_call('clear', shell=True)

    @staticmethod
    def mentum(to_mentum: int, nav_command: str) -> int:
        """Given '+' or '-' from menus, increment or decrement by one. Used to nav pages\n
        (Name from latin root of mentum)"""
        mentums = {'+': '__add__', '-': '__sub__'}
        # method: str = '__%s__' %
        return getattr(to_mentum, mentums[nav_command])(1)

    # Recall that indicators are stored as these strings to represent booleans
    # Display should not have to process bools
    @staticmethod
    def flip_indicator(to_flip) -> str:
        """Used to flip selection indications"""
        return '(*)' if to_flip == '( )' else '( )'


class StaticsFactory:
    """Factory module to generate a Terminal object for pycolims"""
    @staticmethod
    def _return_statics_obj():
        return Statics

    def new_setting_obj(self):
        return self._return_statics_obj()
