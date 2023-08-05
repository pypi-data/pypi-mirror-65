import unittest

from src.sudoku.solver import Sudoku


class TestSudokuSolver(unittest.TestCase):

    def test_solver(self):
        for grid in grids:
            sudoku = Sudoku(grid)
            self.assertTrue(sudoku.solve(), 'Grid should have solution.')
            for row in sudoku.grid:
                self.assertTrue(all(i != 0 for i in row), 'Grid should have no 0s.')


grids = [
    [
        [0, 2, 5, 7, 0, 0, 8, 6, 0],
        [0, 6, 0, 0, 0, 0, 4, 0, 2],
        [0, 4, 0, 9, 0, 0, 3, 0, 0],
        [5, 1, 9, 0, 3, 8, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [4, 0, 0, 6, 9, 0, 2, 5, 8],
        [0, 0, 4, 0, 0, 9, 0, 3, 0],
        [3, 0, 1, 0, 0, 0, 0, 2, 0],
        [0, 9, 6, 0, 0, 4, 5, 8, 0]
    ],
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
]
