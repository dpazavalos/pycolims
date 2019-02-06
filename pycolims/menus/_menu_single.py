from pycolims.data._menu_engine import MenuEngine


class SelectSingle(MenuEngine):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n"""

    def display_line(self, to_display) -> str:
        """Used to generate items into appropriate rows"""
        return ' '.join((f'({to_display[0]})'.rjust(5),
                         f'{to_display[1]}'))

    def prep_page(self):
        """Use self.page.set to prepare page turners"""
        input(self.generate_goto_multipliers())
        self.page.set(page_options=['<>'],
                      goto_multipliers=self.generate_goto_multipliers())

    def prep_given_list(self):
        """Modify self.menu_list, inserting index [orig_ndx, *desired_item(s)]"""
        for ndx, item in enumerate(self.given_list):
            try:
                # inserting index number at beginning of nested list
                self.given_list[ndx].insert(0, ndx)
            except AttributeError:
                # item is not a list. Turn to list with index at beginning
                self.given_list[ndx] = [ndx, self.given_list[ndx]]

    def navigator(self):
        """Select Single Navigator
        Sizes list according to term height, navigates pages, returns a single selection"""

        self.prep_given_list()
        self.prep_page()

        while self.repeating:
            disp_start: int = self.page.goto_multi * self.term.height

            command = self.displayer(self.given_list[disp_start:disp_start+self.term.height])

            try:
                self.command.handler(command)
            except KeyError:
                selected_val = self.given_list[int(command)][1::]
                if len(selected_val) == 1:
                    return selected_val[0]
                return selected_val


class SelectSingleFactory:
    """Factory module to create Single menu obj"""

    @staticmethod
    def _return_single_menu_obj():
        return SelectSingle()

    def new_single_menu_obj(self):
        to_return = self._return_single_menu_obj()
        to_return.set()
        return to_return
