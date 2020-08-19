from pycolims.menus._menu_engine import MenuEngine


class SelectMulti(MenuEngine):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n"""

    def display_line(self, to_display: list) -> None:
        for disp_line in to_display:
            to_print = f'({disp_line[0]})'.rjust(5)
            to_print += '(*)' if disp_line[1] is True else '( )'
            for ndx, each in enumerate(disp_line):
                if ndx not in [0, 1]:
                    to_print += f' {each} '
            print(to_print)

    def prep_page(self):
        """Use self.page.set to prepare page turners"""
        self.page.set(page_options=self.command.multi_def,
                      goto_multipliers=self.generate_goto_multipliers())

    def prep_given_list(self):
        """Modify self.menu_list, preserving index [orig_ndx, bool, *desired_item(s)]"""
        for ndx, item in enumerate(self.work.given_list):
            if isinstance(item, list):
                if isinstance(item[0], bool):
                    self.work.given_list[ndx] = [ndx, item[0], item[1]]
            else:
                self.work.given_list[ndx] = [ndx, False, item]

    def flip_given_list_item(self, ndx):
        self.work.given_list[int(ndx)][1] = not (self.work.given_list[int(ndx)][1])

    def navigator(self) -> list:
        """Select Multiple Navigator
        Sizes list according to term height, navigates pages,
        flips ( ) indicator based off displayer's return value"""

        self.prep_given_list()
        self.prep_page()

        while self.work.repeating:
            disp_start = self.page.goto_multi * self.term.height

            command = self.displayer(self.work.given_list[disp_start:disp_start+self.term.height])
            '''DataCommands is the returned from displayer, either a nav option or an item to trigger'''

            try:
                self.command_handler(command)
            except KeyError:
                self.flip_given_list_item(command)

        return [x[1::] for x in self.work.given_list]


class SelectMutliFactory:
    """Factory module to create Single menu obj"""

    @staticmethod
    def _return_multi_menu_obj():
        return SelectMulti()

    def new_multi_menu_obj(self):
        return self._return_multi_menu_obj()
