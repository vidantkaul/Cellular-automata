


class Grid1D:
    """
        size defines the grid extent, rule is a number: 0 <= r <= 255 using Stephan Wolfram's scheme
    """
    ALIVE = True
    DEAD  = False

    def __init__(self, **kwargs):
        self._size  = kwargs.get('size', 128)
        self._rule  = kwargs.get('rule', 28)
        self._start = kwargs.get('start', -1)

        if self._size < 4:
            raise ValueError(f'Size of Grid1D should be >= 4, got {self._size} instead!')
        if self._rule < 0 or self._rule > 255:
            raise ValueError(f'Rule of Grid1D should be [0, 255]; got {self._rule} instead!')

        self._cells = [self.DEAD for i in range(self._size)]
        if self._start != -1:
            if self._start < 0 or self._start >= self._size:
                raise ValueError(f'Start of Grid1D should be [0, {self._size}); got {self._start} instead!')
            self._cells[self._start] = self.ALIVE
            pass
        else:
            self._cells[self._size // 2] = self.ALIVE

        self._rule_tbl = list(reversed([int(x) for x in f"{self._rule:08b}"]))


    def __str__(self):
        cellstr = "".join(["x" if c else " " for c in self._cells])
        return "|" + cellstr + "|"


    def update(self) -> int:
        next_cells = []
        for i in range(self._size):
            b2 = int(self._cells[i-1]) if i > 0 else 0
            b1 = int(self._cells[i])
            b0 = int(self._cells[i+1]) if i < self._size - 1 else 0
            v = 4*b2 + 2*b1 + b0
            c = self.ALIVE if self._rule_tbl[v] == 1 else self.DEAD
            next_cells.append(c)
        if next_cells == self._cells:
            return -1
        else:
            self._cells = next_cells
            return 0



if __name__ == '__main__':

    g = Grid1D(size=64, rule=78, start=63)
    for time in range(700):
        print(f"{time:03d} {g}")
        ret = g.update()
        if ret == -1:
            print("Simulation Stable, Stopped!!")
            break