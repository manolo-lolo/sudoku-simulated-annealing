from src.sudoku_annealing.data import hard_1
from src.sudoku_annealing.sudoku import assert_sudoku_is_valid_and_get_length


def test_hard_1_is_valid():
    assert_sudoku_is_valid_and_get_length(hard_1)
