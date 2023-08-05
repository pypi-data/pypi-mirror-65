from typing import List, Iterable


class Sudoku:

    def __init__(self, grid: List[List[int]]):
        self.grid = [row[:] for row in grid]

    def row(self, y: int) -> List[int]:
        return self.grid[y]

    def col(self, x: int) -> Iterable[int]:
        return (self.grid[i][x] for i in range(9))

    @staticmethod
    def __in(n: int, i: int) -> bool:
        div = (i // 3) * 3
        return div < n < div + 3

    def square(self, x: int, y: int) -> Iterable[int]:
        return (self.grid[j][i] for j in range(9) for i in range(9) if self.__in(j, y) and self.__in(i, x))

    def possible(self, y: int, x: int, n: int) -> bool:
        return n not in self.row(y) and n not in self.col(x) and n not in self.square(x, y)

    def solve(self) -> bool:
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n):
                            self.grid[y][x] = n
                            if self.solve():
                                return True
                            self.grid[y][x] = 0
                    return False
        return True
