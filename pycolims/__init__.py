name = 'pycolims'


class Single:
    from pycolims.menus.Menu_Factory import build_single, SingleMenu
    run: SingleMenu.run

    def __init__(self):
        single = self.build_single.new_single_menu_obj()
        self.run = single.run


class Multi:
    from pycolims.menus.Menu_Factory import MultiMenu, build_multi
    run: MultiMenu.run

    def __init__(self, ):
        multi = self.build_multi.new_multi_menu_obj()
        self.run = multi.run
