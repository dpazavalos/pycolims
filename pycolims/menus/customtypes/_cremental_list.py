"""Extension of default list obj. Adds a tracking index for an 'active' item

get_active() -> any:
    Returns item from list using active ndx

set_ndx(new_ndx: int) -> None
    Attempts to set active ndx.
    Raises a Value Error if given ndx is outside list ndx

crement(cmd: str, return_value=False) -> Optional[int]:
    Attempts to increment or decrement
"""


class CrementalList(list):
    """Extention of default list obj. Adds a tracking index for an 'active' item"""

    ndx: int = 0

    def get_active(self) -> any:
        """Returns item from list using active ndx"""
        return self[self.ndx]

    def get_ndx(self) -> int:
        """Returns active ndx"""
        return self.ndx

    def set_ndx(self, new_ndx: int) -> None:
        """Attempts to set active ndx.
        Raises a Value Error if given ndx is outside list ndx"""
        if new_ndx < 0 or new_ndx > self.__len__():
            raise ValueError(f'new ndx is outside of list length 0-{self.__len__()}!')
        else:
            self.ndx = new_ndx

    def crement(self, crementer: str, return_ndx=False) -> int:
        """attempts in increment or decrement active ndx by 1, within list boundaries\n
        Returns new active ndx"""
        _menters: dict = {'+': self.increment, '-': self.decrement}
        if crementer not in _menters:
            raise KeyError(f"Invalid crementer! \n {_menters}")

        _menters[crementer]()
        if return_ndx is True:
            return self.get_ndx()

    def increment(self):
        """Safe ndx incrementer"""
        if self.ndx + 1 < self.__len__():
            self._ndx_i()

    def decrement(self):
        """Safe ndx decrementer"""
        if self.ndx - 1 >= 0:
            self._ndx_d()

    def _ndx_i(self):
        """Increment ndx +1"""
        self.ndx += 1

    def _ndx_d(self):
        """Decrement ndx -1"""
        self.ndx -= 1
