class MentumList(list):
    goto: int = 0

    def get_active(self) -> any:
        return self[self.goto]

    def set_goto(self, new_goto: int):
        if 0 > new_goto or new_goto > self.__len__():
            raise ValueError(f'new goto is outside of list length 0-{self.__len__()}!')
        else:
            self.goto = new_goto

    def mentum(self, cmd: str, return_val=True) -> int:
        """attempts in increment or decrement active goto by 1, within list boundaries\n
        Returns new active goto value"""
        _menters: dict = {'+': self.increment,
                          '-': self.decrement}
        if cmd not in _menters:
            raise KeyError(f"Invalid mentum key! \n {_menters}")
        else:
            _menters[cmd]()
        if return_val is True:
            return self.goto

    def increment(self):
        """Safe goto incrementer"""
        if self.goto + 1 < self.__len__():
            self._goto_i()

    def decrement(self):
        """Safe goto decrementer"""
        if self.goto - 1 >= 0:
            self._goto_d()

    def _goto_i(self):
        """Increment goto +1"""
        self.goto += 1

    def _goto_d(self):
        """Decrement goto -1"""
        self.goto -= 1
