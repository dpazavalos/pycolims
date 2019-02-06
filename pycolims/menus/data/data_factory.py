from pycolims.data import _data_pages, _data_terminal, _data_cmd, _data_work


class Command(_data_cmd.Command):
    """Generic dataclass for Commands"""


class Pages(_data_pages.Pages):
    """Generic dataclass for page settings"""


class Terminal(_data_terminal.Terminal):
    """Generic dataclass for terminal settings"""


class Work(_data_work.Work):
    """Genric dataclass for Work hold"""


class _Factory(_data_terminal.TermFactory, _data_pages.PageFactory,
               _data_cmd.CommandFactory, _data_work.WorkFactory):
    """Factory to build dataclass objects"""


build = _Factory()
"""Externally callable pointer to init factory"""
