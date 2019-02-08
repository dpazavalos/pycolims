from pycolims.menus import _menu_single, _menu_multi


class SingleMenu(_menu_single.SelectSingle):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n"""


class MultiMenu(_menu_multi.SelectMulti):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n
    Once init, call run()"""


class _FactorySingle(_menu_single.SelectSingleFactory, ):
    """Importable single menu builder"""


class _FactoryMulti(_menu_multi.SelectMutliFactory, ):
    """Importable multi menu builder"""


build_single = _FactorySingle()
"""Externally callable pointer to init factory"""

build_multi = _FactoryMulti()
"""Externally callable pointer to init factory"""
