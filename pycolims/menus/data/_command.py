"""Commands used by navigator"""

from pycolims.menus._base_menu_template import MenuTemplate
# Command requires knowledge of some base menu functions. Import template to match plans when
# loaded into Factory generated menu


class Command(MenuTemplate):

    turners: dict = None
    options: dict = None
    turners_inv: dict = None
    options_inv: dict = None

    single_def: list = None
    multi_def: list = None

    def set(self):
        """Set command obj stats"""
        # Phase obj to frozen dataclass, and move set to local CommandFactory?
        self.turners = {
            ' ': " ",
            '-': "Prev Page",
            '+': "Next Page",
        }
        """Possible menu choices to change pages"""
        self.options = {
            '**': "Select All",
            '//': "Clear All",
            '><': "Flip All",
            '..': "Return Selected",
            '!!': "Break",
        }
        """Possible menu choices to change pages"""
        self.turners_inv = {val: key for key, val in self.turners.items()}
        """Dict enforcement of page turner; call by Values"""
        self.options_inv = {val: key for key, val in self.options.items()}
        """Dict enforcement of page turner; call by Values"""

        self.single_def = [
            self.options_inv["Break"],
        ]
        """default options keys for single menus"""
        self.multi_def = [
            self.options_inv["Select All"],         # **
            self.options_inv["Clear All"],          # //
            self.options_inv["Flip All"],           # ><
            self.options_inv["Return Selected"],    # ..
            self.options_inv["Break"]               # !!
        ]
        """default options keys for multi menus"""


class CommandFactory:
    """Factory module to generate a Command obj for Pycolims"""

    @staticmethod
    def _return_command_obj():
        return Command()

    def new_command_obj(self):
        to_return = self._return_command_obj()
        to_return.set()
        return to_return
