from pycolims._basemenu import _Menu


class SelectMulti(_Menu):
    """Given a list, prompt for selection of items in a list.\n
    Returns a list with nested booleans indicating if selected or not\n
    [item for [boolean, item] in menu.run(menu_in) if boolean]\n\n
    Once init, call run()"""

    def display_line(self, to_display: str) -> str:
        return ' '.join((f'({to_display[0]})'.rjust(5),
                         '(*)' if to_display[1] is True else '( )',
                         f'{to_display[2]}'))

    def prep_page(self):
        """Use self.page.reset to prepare page turners"""
        self.page.reset(only_turners=[],
                        frst_turners=['+'],
                        midl_turners=['-', '+'],
                        last_turners=['-', ],
                        page_options=['**', '!!', '..', '<>'],
                        goto_multipliers=self.generate_goto_multipliers())

    def navigator(self) -> list:
        """Select Multiple Navigator
        Sizes list according to term height, navigates pages,
        flips ( ) indicator based off displayer's return value"""

        # Modify self.menu_list, preserving index [orig_ndx, *desired_item(s)]
        for ndx, item in enumerate(self.given_list):
            if isinstance(item, list):
                if isinstance(item[0], bool):
                    # sbool = '(*)' if self.given_list[ndx][0] is True else '( )'
                    self.given_list[ndx] = [ndx, item[0], item[1]]
            else:
                self.given_list[ndx] = [ndx, False, item]

        command = ""
        '''Command is the returned str from displayer, either a nav option or an item to trigger'''

        # Call Displayer to determine necessary selection(s)
        self.term.clear()
        while command != "..":
            disp_start = self.page.goto_multi * self.term.height
            command = self.displayer(self.given_list[disp_start: disp_start + self.term.height],
                                     self.page.active_turners)

            # Try 'doing' the returned value (by index integer)
            if not self.valid_option(command):
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
