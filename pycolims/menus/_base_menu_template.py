from typing import List, Dict, Tuple, Union


class MenuTemplate:

    # given_list = None
    """Menu to break and display"""

    # header: str = ""
    """Optional Header, assigned from each menu's run function"""

    # repeating: bool = True
    """Repeating flag used keep navigators open"""

    term: any = None
    page: any = None
    command: any = None

    def generate_goto_multipliers(self) -> List[int]:
        """Returns a list of valid index start places based off terminal height\n
        Used to configure page data"""

    def displayer(self, itemlist: List[List[str]]) -> str:
        """Called by a Navigator function, displays a given list on screen, along with nav options\n
        Selected option must be one shown on screen"""

    def display_line(self, to_display: Union[List, Tuple]) -> str:
        """creates a display line for displayer. Modified by menu types"""

    def option_line(self, option: str) -> str:
        """creates an option line for displayer"""

    def retype_given_list(self, to_handle: Union[list, tuple, dict]):
        """Prepare menu_in into proper type """

    def navigator(self) -> list:
        """Function to handle handoff of menu_in items to displayer\n
        This function is rewritten for each menu type"""

    def run(self,
            given_list: Union[List[any],
                              List[Tuple[bool, any]],
                              Tuple[any],
                              Dict[any, any]],
            header: str = "") -> Union[any,
                                       List[any],
                                       List[Tuple[bool, any]]]:
        """Given a list, prompt for selection of item or items in a list.\n
        Returns a list with nested booleans indicating if selected or not\n
        [item for [boolean, item] in menu.run(menu_in) if boolean]"""
