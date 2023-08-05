import unittest

from mgsolver.ball_sort_puzzle.solver import BallSortPuzzle
from mgsolver.ball_sort_puzzle.color import Color


class TestBallSortPuzzleSolver(unittest.TestCase):

    def test_all_levels_valid(self):
        for level in levels.keys():
            ball_sort_puzzle = BallSortPuzzle(levels[level])
            self.assertNotEqual(ball_sort_puzzle.cells_len, 0, f'Level {level} is invalid.')

    def test_level_validation(self):
        # valid
        BallSortPuzzle([[0, 0, 0], [0]])
        BallSortPuzzle([[0, 1, 2, 1], [1, 1, 2, 0], [2, 2], [0, 0], []])

        # finished
        BallSortPuzzle([[0, 0, 0, 0]])
        BallSortPuzzle([[0, 0, 0, 0], [1, 1, 1, 1], []])

        # empty
        BallSortPuzzle([[]])
        BallSortPuzzle([[], [], []])

        # not default max_in_cell
        BallSortPuzzle([[0, 0], [0]], max_in_cell=3)
        BallSortPuzzle([[0, 1, 1], [0, 1, 0], []], max_in_cell=3)

        # invalid number
        self.assertRaises(Exception, lambda: BallSortPuzzle([[0, 0], [0]]),
                          'Level should be invalid if not all the colors are in number of 4.')
        self.assertRaises(Exception, lambda: BallSortPuzzle([[0, 1], [0], []]),
                          'Level should be invalid if not all the colors are in number of 4.')

        # not enough number of cells for all the colors
        self.assertRaises(Exception, lambda: BallSortPuzzle([[0, 1, 2, 3]], max_in_cell=1),
                          'Level should be invalid if not enough cells for all the colors.')

    def test_all_levels(self):
        for level in filter(lambda i: i < 10, levels.keys()):
            print(f'\nTESTING LEVEL {level}\n')
            ball_sort_puzzle = BallSortPuzzle(levels[level])
            self.assertTrue(ball_sort_puzzle.solve(), f'Did not solve level {level}.')
            print('=' * 25)

    def test_level(self):
        level = 103
        ball_sort_puzzle = BallSortPuzzle(levels[level])
        self.assertTrue(ball_sort_puzzle.solve(), f'Did not solve level {level}.')


levels = {
    1: [
        [Color.orange],
        [Color.orange, Color.orange, Color.orange]
    ],
    2: [
        [Color.blue, Color.orange, Color.blue, Color.orange],
        [Color.orange, Color.blue, Color.orange, Color.blue],
        []
    ],
    3: [
        [Color.blue, Color.orange, Color.red, Color.blue],
        [Color.orange, Color.orange, Color.red, Color.blue],
        [Color.red, Color.blue, Color.orange, Color.red],
        [],
        []
    ],
    4: [
        [Color.blue, Color.red, Color.orange, Color.orange],
        [Color.blue, Color.red, Color.blue, Color.red],
        [Color.orange, Color.blue, Color.red, Color.orange],
        [],
        []
    ],
    5: [
        [Color.lightgreen, Color.orange, Color.blue, Color.pink],
        [Color.orange, Color.lightgreen, Color.blue, Color.pink],
        [Color.pink, Color.red, Color.orange, Color.red],
        [Color.orange, Color.pink, Color.red, Color.blue],
        [Color.lightgreen, Color.lightgreen, Color.red, Color.blue],
        [],
        [],
    ],
    6: [
        [Color.red, Color.lightgreen, Color.lightgreen, Color.lightgreen],
        [Color.orange, Color.red, Color.pink, Color.lightgreen],
        [Color.pink, Color.orange, Color.red, Color.orange],
        [Color.blue, Color.pink, Color.orange, Color.pink],
        [Color.blue, Color.blue, Color.blue, Color.red],
        [],
        [],
    ],
    7: [
        [Color.lightgreen, Color.orange, Color.red, Color.orange],
        [Color.blue, Color.blue, Color.red, Color.orange],
        [Color.pink, Color.pink, Color.blue, Color.orange],
        [Color.lightgreen, Color.pink, Color.red, Color.blue],
        [Color.lightgreen, Color.red, Color.lightgreen, Color.pink],
        [],
        [],
    ],
    8: [
        [Color.lightgreen, Color.orange, Color.lightgreen, Color.blue],
        [Color.orange, Color.pink, Color.pink, Color.orange],
        [Color.pink, Color.red, Color.blue, Color.red],
        [Color.blue, Color.red, Color.lightgreen, Color.pink],
        [Color.blue, Color.lightgreen, Color.red, Color.orange],
        [],
        [],
    ],
    9: [
        [Color.pink, Color.red, Color.blue, Color.pink],
        [Color.red, Color.lightgreen, Color.lightgreen, Color.orange],
        [Color.red, Color.orange, Color.orange, Color.pink],
        [Color.pink, Color.red, Color.lightgreen, Color.blue],
        [Color.lightgreen, Color.orange, Color.blue, Color.blue],
        [],
        [],
    ],
    10: [
        [Color.pink, Color.blue, Color.lightgreen, Color.blue],
        [Color.orange, Color.gray, Color.pink, Color.red],
        [Color.blue, Color.lightblue, Color.lightblue, Color.lightgreen],
        [Color.pink, Color.orange, Color.orange, Color.lightgreen],
        [Color.gray, Color.gray, Color.lightgreen, Color.red],
        [Color.blue, Color.red, Color.lightblue, Color.lightblue],
        [Color.red, Color.pink, Color.orange, Color.gray],
        [],
        [],
    ],
    103: [
        [Color.lightgreen, Color.orange, Color.yellow, Color.lightblue],
        [Color.darkgreen, Color.yellow, Color.green, Color.lightblue],
        [Color.blue, Color.red, Color.lightgreen, Color.purple],
        [Color.gray, Color.red, Color.lightblue, Color.yellow],
        [Color.yellow, Color.blue, Color.pink, Color.darkgreen],
        [Color.green, Color.brown, Color.darkgreen, Color.brown],
        [Color.red, Color.purple, Color.blue, Color.brown],
        [Color.brown, Color.blue, Color.pink, Color.purple],
        [Color.gray, Color.lightgreen, Color.pink, Color.gray],
        [Color.lightblue, Color.green, Color.lightgreen, Color.orange],
        [Color.red, Color.purple, Color.gray, Color.darkgreen],
        [Color.orange, Color.green, Color.orange, Color.pink],
        [],
        []
    ]
}
