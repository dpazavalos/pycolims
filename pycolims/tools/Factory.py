from pycolims.tools import _pagedata, _termsettings


class Terminal(_termsettings.Terminal):
    """Generic dataclass for terminal settings"""


class Pages(_pagedata.Pages):
    """Generic dataclass for page settings"""


class _Factory(_termsettings.TermFactory, _pagedata.PageFactory, ):
    """Factory to build dataclass objects"""


build = _Factory()
"""Externally callable pointer to init factory"""
