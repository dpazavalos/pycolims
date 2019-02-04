from pycolims._basemenu import _Menu


class SelectMulti(_Menu):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n
    Once init, call run()"""

    def navigator(self) -> list:
        """Select Multiple Navigator
        Sizes list according to term height, navigates pages,
        flips ( ) indicator based off displayer's return value"""

        self.page.reset(only_turners=[' ', ' '],
                        frst_turners=[' ', '+'],
                        midl_turners=['-', '+'],
                        last_turners=['-', ' '],
                        page_options=['**', '!!', '..', '<>'])

        # Modify self.menu_list, preserving index [orig_ndx, *desired_item(s)]
        # Bools are converted to strings T '(*)', F '( )'
        for ndx in range(len(self.given_list)):

            if isinstance(self.given_list[ndx], list):
                if isinstance(self.given_list[ndx][0], bool):
                    sbool = '(*)' if self.given_list[ndx][0] is True else '( )'
                    self.given_list[ndx] = [ndx, sbool, self.given_list[ndx][1]]

            else:
                self.given_list[ndx] = [ndx, '( )', self.given_list[ndx]]

        goto_multipliers = self.generate_goto_multipliers()
        nav_options = self.generate_nav_options(goto_multipliers)

        # Used to determine which section of menu_list to send
        goto_multi = 0  # Multiply by self.term_height to determine starting index
        command = ""
        '''Command is the returned str from displayer, either a nav option or an item to trigger'''

        # Call Displayer to determine necessary selection(s)
        self.clear_screen()
        while command != "..":
            disp_start = goto_multi * self.term_height
            command = self.displayer(self.given_list[disp_start: disp_start + self.term_height],
                                     nav_options[goto_multi])

            # Try 'doing' the returned value (by index integer)
            if not self.valid_navigator(command):
                # Execute based on selection
                self.given_list[int(command)][1] = \
                    self.flip_indicator(self.given_list[int(command)][1])

            # Select All
            if command == '?':
                for entry in self.given_list:
                    entry[1] = '(*)'

            # Clear All
            if command == '!':
                for entry in self.given_list:
                    entry[1] = '( )'

            else:  # Try navigating between chunks (by '+' or '-' characters)
                try:
                    if self.mentum(goto_multi, command) in goto_multipliers:
                        goto_multi = self.mentum(goto_multi, command)
                except KeyError:
                    pass

        return [
            [(x[1] == '(*)')] + x[2::]
            for x in self.given_list
        ]  # recall that x[0] was our index, Not needed.
