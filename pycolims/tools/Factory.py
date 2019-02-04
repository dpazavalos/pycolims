from pycolims.tools import _pagedata, _statics, _termsettings


class Terminal(_termsettings.Terminal):
    """Generic dataclass for terminal settings"""


class Statics(_statics.Statics):
    """Generic dataclas for common static tools"""


class Pages(_pagedata.Pages):
    """Generic dataclass for page settings"""


class Factory(_termsettings.TermFactory, _pagedata.PageFactory, _statics.StaticsFactory):
    """Factory to build dataclass objects"""
