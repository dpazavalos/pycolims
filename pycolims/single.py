from pycolims._basemenu import _Menu
from typing import List, Tuple


class SelectSingle(_Menu):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n"""

    def prep_page(self):
        """Use self.page.reset to prepare page turners"""
        self.page.reset(only_turners=[],
                        frst_turners=['+'],
                        midl_turners=['-', '+'],
                        last_turners=['-', ],
                        page_options=['<>'],
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

    def command_handler(self, command: str):
        handler = {self.command_check.options_inv["Break"]: self._cmd_break}
        handler[command]()

    def _cmd_break(self):
        raise KeyboardInterrupt

    def navigator(self):
        """Select Single Navigator
        Sizes list according to term height, navigates pages, returns a single selection"""

        self.prep_given_list()
        self.prep_page()

        # goto_multipliers: List[int] = self.generate_goto_multipliers()
        # nav_options: List[List[List[str]]] = self.generate_nav_options(goto_multipliers)
        # goto_multi = 0
        """Multiply by self.term_height to determine starting index"""

        self.term.clear()

        selected_val = ''
        while selected_val == '':
            disp_start: int = self.page.goto_multi * self.term.height

            command = self.displayer(self.given_list[disp_start:disp_start+self.term.height],
                                     self.page.active_turners)
            """Command is the returned str from displayer (nav option or a single menu selection)"""

            if command in ['+', '-']:
                self.page.mentum(command)

            elif self.valid_option(command):
                self.command_handler(command)
                pass
            else:
                selected_val = self.given_list[int(command)][1::]

        if len(selected_val) == 1:
            return selected_val[0]
        return selected_val
