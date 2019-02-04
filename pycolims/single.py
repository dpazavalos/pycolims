from pycolims._basemenu import _Menu
from typing import List, Dict, Tuple, Union


class SelectSingle(_Menu):
    """Given a list, prompt for selection of a single item\n
    Returns the selected item\n
    List can be flat or an array\n\n
    Once init, call run()"""

    def navigator(self):
        """Select Single Navigator
        Sizes list according to term height, navigates pages, returns a single selection"""

        self.page.reset(only_turners=[' ', ' '],
                        frst_turners=[' ', '+'],
                        midl_turners=['-', '+'],
                        last_turners=['-', ' '],
                        page_options=['..', '<>'])

        # Modify self.menu_list, inserting index [orig_ndx, *desired_item(s)]
        for ndx in range(len(self.given_list)):
            try:
                # inserting index number at beginning of nested list
                self.given_list[ndx].insert(0, ndx)
            except AttributeError:
                # item is not a list. Turn to list with index at beginning
                self.given_list[ndx] = [ndx, self.given_list[ndx]]
            except KeyError:
                print(type(self.given_list))
                print(self.given_list)
                exit(1)

        goto_multipliers: List[int] = self.generate_goto_multipliers()
        nav_options: List[List[Tuple[str]]] = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0
        """Multiply by self.term_height to determine starting index"""

        self.clear_screen()
        while True:
            disp_start: int = goto_multi * self.term_height

            command = self.displayer(self.given_list[disp_start: (disp_start + self.term_height)],
                                     nav_options[goto_multi])
            """Command is the returned str from displayer (nav option or a single menu selection)"""

            if not self.valid_navigator(command):
                selected_val = self.given_list[int(command)][1::]
                """Selection pulled from menu_list, based on command. Value to be returned"""
                break

            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.mentum(goto_multi, command)
                except (KeyError, IndexError):
                    # Key and Index errors cover the possible "Next page when last page"
                    pass

        return selected_val[0] if len(selected_val) == 1 else selected_val