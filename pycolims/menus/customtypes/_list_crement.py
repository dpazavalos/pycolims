"""Extention of default list obj. Adds a tracking index for an 'active' item

get_active() -> any:
    Returns item from list using active ndx

set_ndx(new_ndx: int) -> None
    Attempts to set active ndx.
    Raises a Value Error if given ndx is outside list ndx

crement(cmd: str, return_value=False) -> Optional[int]:
    Attempts to increment or decrement
"""


class ListCrement(list):

    def __init__(self, incrememter='+', decrementer='-'):
        super().__init__()

        self._menters: dict = {incrememter: self.increment,
                               decrementer: self.decrement}
        '''string keys to '''
        self.ndx: int = 0

    def get_active(self) -> any:
        return self[self.ndx]

    def set_ndx(self, new_ndx: int) -> None:
        if 0 > new_ndx or new_ndx > self.__len__():
            raise ValueError(f'new ndx is outside of list length 0-{self.__len__()}!')
        else:
            self.ndx = new_ndx

    def crement(self, crementer: str, return_ndx=False) -> any:
        """attempts in increment or decrement active ndx by 1, within list boundaries\n
        Returns new active ndx"""
        if crementer not in self._menters:
            raise KeyError(f"Invalid crementer! \n {self._menters}")
        else:
            self._menters[crementer]()
        if return_ndx is True:
            return self.ndx

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
