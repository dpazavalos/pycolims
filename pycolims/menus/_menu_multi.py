from pycolims.data._menu_engine import MenuEngine


class SelectMulti(MenuEngine):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n
    Once init, call run()"""

    def display_line(self, to_display: str) -> str:
        return ' '.join((f'({to_display[0]})'.rjust(5),
                         '(*)' if to_display[1] is True else '( )',
                         f'{to_display[2]}'))

    def prep_page(self):
        """Use self.page.set to prepare page turners"""
        self.page.set(page_options=['**', '!!', '..', '<>'],
                      goto_multipliers=self.generate_goto_multipliers())

    def prep_given_list(self):
        """Modify self.menu_list, preserving index [orig_ndx, bool, *desired_item(s)]"""
        for ndx, item in enumerate(self.given_list):
            if isinstance(item, list):
                if isinstance(item[0], bool):
                    self.given_list[ndx] = [ndx, item[0], item[1]]
            else:
                self.given_list[ndx] = [ndx, False, item]

    def navigator(self) -> list:
        """Select Multiple Navigator
        Sizes list according to term height, navigates pages,
        flips ( ) indicator based off displayer's return value"""

        self.prep_given_list()
        self.prep_page()

        command = ""
        '''Command is the returned str from displayer, either a nav option or an item to trigger'''

        # self.term.clear()
        while self.repeating:
            disp_start = self.page.goto_multi * self.term.height

            command = self.displayer(self.given_list[disp_start: disp_start + self.term.height])

            try:
                self.command.handler(command)
            except KeyError:
                self.given_list[int(command)][1] = not (self.given_list[int(command)][1])

        # return [ [bool] for x in self.given_list]

        return [[x[1::]] for x in self.given_list]


class SelectMutliFactory:
    """Factory module to create Single menu obj"""

    @staticmethod
    def _return_multi_menu_obj():
        return SelectMulti()

    def new_multi_menu_obj(self, list_to_give, header):
        to_return = self._return_multi_menu_obj()
        to_return.set(list_to_give, header)
        return to_return
