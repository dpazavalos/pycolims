"""Commands used by navigator.
Pycolims uses the key characters to function; string values are for on screen representation
Emulation of 3.7 frozen dataclasses.
Once init, set/del function calls will throw SyntaxError to enforce soft immutability"""


class Command:
    """External storage of string command keys to full names.
    Default command options for child menus"""

    turners: dict = None
    options: dict = None
    turners_inv: dict = None
    options_inv: dict = None

    single_def: list = None
    multi_def: list = None

    _frozen: bool = False

    def __init__(self):

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

        self._frozen = True
        """Lock attributes after init"""

    def __setattr__(self, item, value):
        """Pre 3.7 emulation of frozen dataclasses. Soft mutation prevention"""
        if self._frozen:
            raise SyntaxError("Consider Command obj immutable, do not modify!")
        self.__dict__[item] = value

    def __delattr__(self, item):
            """Pre 3.7 emulation of frozen dataclasses. Soft mutation prevention"""
            if self._frozen:
                raise SyntaxError("Consider Command obj immutable, do not modify!")
            del self.__dict__[item]


class CommandFactory:
    """Factory module to generate a Command obj for pycolims"""

    @staticmethod
    def _return_command_obj():
        return Command()

    def new_command_obj(self):
        to_return = self._return_command_obj()
        return to_return
