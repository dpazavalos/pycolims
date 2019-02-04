from pycolims._basemenu import _Menu
from typing import List, Tuple


class SelectSingle(_Menu):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n
    List can be flat or an array\n\n
    Once init, call run()"""

    def prep_page(self):
        """Use self.page.reset to prepare page turners"""
        self.page.reset(only_turners=[' ', ' '],
                        frst_turners=[' ', '+'],
                        midl_turners=['-', '+'],
                        last_turners=['-', ' '],
                        page_options=['<>'])

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

        self.prep_page()
        self.prep_given_list()

        goto_multipliers: List[int] = self.generate_goto_multipliers()
        nav_options: List[List[List[str]]] = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0
        """Multiply by self.term_height to determine starting index"""

        self.statics.clear_screen()
        while True:
            disp_start: int = goto_multi * self.term.height

            command = self.displayer(self.given_list[disp_start: (disp_start + self.term.height)],
                                     nav_options[goto_multi])
            """Command is the returned str from displayer (nav option or a single menu selection)"""

            if not self.valid_navigator(command):
                selected_val = self.given_list[int(command)][1::]
                """Selection pulled from menu_list, based on command. Value to be returned"""
                break

            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.statics.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.statics.mentum(goto_multi, command)
                except (KeyError, IndexError):
                    # Key and Index errors cover the possible "Next page when last page"
                    pass

        if len(selected_val) == 1:
            return selected_val[0]
        return selected_val
