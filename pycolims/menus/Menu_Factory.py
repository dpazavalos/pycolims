from pycolims.data import _menu_single, _menu_multi


class SingleMenu(_menu_single.SelectSingle):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n"""


class MultiMenu(_menu_multi.SelectMulti):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n
    Once init, call run()"""


class _Factory(_menu_single.SelectSingleFactory, _menu_multi.SelectMutliFactory):
    """Generic Factory obj"""


build = _Factory()
"""Externally callable pointer to init factory"""


class Single:
    @staticmethod
    def run(list_to_give):
        to_run = build.new_single_menu_obj()
        return to_run.run(list_to_give)


def multi_run(list_to_give):
    return build.new_multi_menu_obj(list_to_give).run()
