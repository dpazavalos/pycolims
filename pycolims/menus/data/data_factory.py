from pycolims.menus.data import _command, _terminal, _work, _pages


class Command(_command.Command):
    """Generic dataclass for Commands"""


class Pages(_pages.Pages):
    """Generic dataclass for page settings"""


class Terminal(_terminal.Terminal):
    """Generic dataclass for terminal settings"""


class Work(_work.Work):
    """Generic dataclass for Work hold"""


class DataFactory(_terminal.TermFactory, _pages.PageFactory,
                  _command.CommandFactory, _work.WorkFactory):
    """Factory to build dataclass-like objects"""


# build = _Factory
"""Externally callable pointer to init factory"""
