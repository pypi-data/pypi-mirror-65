from src.data_resolver import DataResolver
from src.messages import EMPTY_RES_FILE
from src.nonogram_marks import value_to_mark
from src.size import Size


class Solver:
    def __init__(self):
        self.left = DataResolver.get_left_data()
        self.top = DataResolver.get_top_data()
        try:
            self.size = Size(width=len(self.top), height=len(self.left))
        except ValueError:
            raise Exception(EMPTY_RES_FILE)

        self.solution = [[0 for _ in range(self.size.width)] for _ in range(self.size.height)]

    def __str__(self) -> str:
        return '\n'.join('|'.join(value_to_mark(elem) for elem in line) for line in self.solution)

    def solve(self):
        # iterate over lines, keeping its index to access self.solution
        for line_index, line in enumerate(self.left):
            col_index = 0  # keep column index to access self.solution

            # iterate over line, where elem is the number written in line
            for elem in line:
                # fill solution with the corresponding number
                for i in range(elem):
                    self.solution[line_index][col_index + i] = 1
                col_index += elem  # move col_index behind filled line

                # if there is still a place, write an X mark behind the line
                if col_index < self.size.width:
                    self.solution[line_index][col_index] = -1
                col_index += 1  # move index behind the X mark
