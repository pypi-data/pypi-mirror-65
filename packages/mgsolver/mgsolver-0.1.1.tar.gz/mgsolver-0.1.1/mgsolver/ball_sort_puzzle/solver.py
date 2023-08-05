from .color import Color
from typing import List


class BallSortPuzzle:

    def __init__(self, cells: List[List[int]], max_in_cell=4):
        self.cells = cells
        self.max_in_cell = max_in_cell
        self.validate()

    def validate(self):
        colors = {}
        for cell in self.cells:
            for color in cell:
                if color in colors.keys():
                    colors[color] += 1
                else:
                    colors[color] = 1

        color_amounts = colors.values()
        if self.cells_len < len(color_amounts) or any(amount != self.max_in_cell for amount in color_amounts):
            self.clear_cells()
            raise Exception('The ball sort level is not valid.')

    @property
    def cells(self):
        return self.__cells

    @cells.setter
    def cells(self, cells):
        self.__cells = [cell[:] for cell in cells]
        self.cells_len = len(self.cells)

    def clear_cells(self):
        self.cells = [[]]

    def finished(self) -> bool:
        for cell in self.cells:
            if len(cell) not in (0, self.max_in_cell):
                return False
            if len(cell) == self.max_in_cell and any(cell[0] != c for c in cell):
                return False
        return True

    def __move(self, color: int, from_index: int, to_index: int):
        self.cells[to_index].append(color)  # append color here
        self.cells[from_index].pop(-1)  # pop from cell

    def __not_empty_cells(self):
        return (i for i in range(self.cells_len) if len(self.cells[i]) > 0)

    def __top_color(self, index: int) -> int:
        return self.cells[index][-1]

    def __possible(self, from_index: int, to_index: int) -> bool:
        # moving from here makes empty cell
        if len(self.cells[from_index]) == 1:
            return True
        for i in range(self.cells_len):
            if i == from_index or i == to_index:
                continue
            if len(self.cells[i]) == 0 or self.cells[from_index][-2] == self.cells[i][-1]\
                    or (self.cells[from_index][-1] and len(self.cells[to_index]) < self.max_in_cell - 1):
                return True
        return False

    def solve(self) -> bool:
        if self.finished():
            return True

        # not empty cells
        for current_index in self.__not_empty_cells():
            current_color = self.__top_color(current_index)
            if any(c != current_color for c in self.cells[current_index]):
                # all other indexes
                for other_index in self.__not_empty_cells():
                    if other_index == current_index:
                        continue
                    # other index not empty and not full
                    other_cell_len = len(self.cells[other_index])
                    if other_cell_len < self.max_in_cell and current_color == self.__top_color(other_index) \
                            and self.__possible(current_index, other_index):
                        self.__move(current_color, from_index=current_index, to_index=other_index)
                        if self.solve():
                            print(f'Moved {Color.to_string(current_color)} from {current_index} to {other_index}')
                            return True
                        self.__move(current_color, from_index=other_index, to_index=current_index)

                empty_cells = [i for i in range(self.cells_len) if len(self.cells[i]) == 0]
                if len(empty_cells) > 0:
                    self.__move(current_color, from_index=current_index, to_index=empty_cells[0])
                    if self.solve():
                        print(f'Moved {Color.to_string(current_color)} from {current_index} to {empty_cells[0]}')
                        return True
                    self.__move(current_color, from_index=empty_cells[0], to_index=current_index)

            # same colors here but other cell can have the same colors as well
            else:
                for other_index in self.__not_empty_cells():
                    if other_index == current_index:
                        continue
                    if self.__top_color(other_index) == current_color \
                            and len(self.cells[current_index]) >= len(self.cells[other_index]):
                        self.__move(current_color, from_index=other_index, to_index=current_index)
                        if self.solve():
                            print(f'Moved {Color.to_string(current_color)} from {other_index} to {current_index}')
                            return True
                        self.__move(current_color, from_index=current_index, to_index=other_index)
        # no other movement possible
        return False
