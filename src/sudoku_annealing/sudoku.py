from collections import Counter
from random import shuffle, choice, sample
from typing import List


def count_duplicates(sequence: str) -> int:
    counter = Counter(sequence)
    no_duplicates = sum(
        count - 1 for value, count in counter.items() if count > 1 and value != "0"
    )
    return no_duplicates


def assert_sudoku_is_valid_and_get_length(sudoku: str) -> (int, int):
    no_cols = {len(line) for line in sudoku.split("\n")}
    no_rows = sudoku.count("\n") + 1
    if (
        not set(sudoku) <= {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\n"}
        or len(no_cols) > 1
        or no_rows != list(no_cols)[0]
    ):
        raise ValueError("Sudoku is invalid")
    return no_rows


def get_sudoku_line(sudoku: str, line_no: int) -> str:
    return sudoku.split("\n")[line_no]


def get_sudoku_row(sudoku: str, row_no: int) -> str:
    return "".join(line[row_no] for line in sudoku.split("\n"))


def get_sudoku_quadrant(sudoku: str, quadrant_no: int) -> str:
    quadrant_row_no = quadrant_no // 3
    quadrant_col_no = quadrant_no % 3
    return "\n".join(
        get_sudoku_line(sudoku, row_no)[quadrant_col_no * 3 : quadrant_col_no * 3 + 3]
        for row_no in range(quadrant_row_no * 3, quadrant_row_no * 3 + 3)
    )


def get_sudoku_fixed_mask(sudoku: str) -> str:
    return "".join("\n" if s == "\n" else str(int(s != "0")) for s in sudoku)


def sudoku_quadrant_valid_fill(quadrant: str) -> str:
    counter = Counter(quadrant)
    if "0" not in counter:
        return quadrant
    no_substitutions = counter.pop("0")
    counter.pop("\n")
    assert len(counter) == 0 or counter.most_common(1)[0][1] == 1
    missing_numbers = list(
        {"1", "2", "3", "4", "5", "6", "7", "8", "9"} - set(counter.keys())
    )
    assert len(missing_numbers) == no_substitutions
    shuffle(missing_numbers)
    for missing_number in missing_numbers:
        quadrant = quadrant.replace("0", missing_number, 1)
    return quadrant


def sudoku_replace_quadrant(
    sudoku: str, quadrant_no: int, replacement_quadrant: str
) -> str:
    assert assert_sudoku_is_valid_and_get_length(sudoku) == 9
    quadrant_row_no = quadrant_no // 3
    quadrant_col_no = quadrant_no % 3
    for i, row_no in enumerate(range(quadrant_row_no * 3, quadrant_row_no * 3 + 3)):
        sudoku = (
            sudoku[: row_no * 10 + quadrant_col_no * 3]
            + replacement_quadrant.split()[i]
            + sudoku[row_no * 10 + quadrant_col_no * 3 + 3 :]
        )
    return sudoku


def get_swappable_quadrants(fixed_mask: str) -> List[int]:
    swappable = []
    for quadrant_no in range(9):
        quadrant_fixed_mask = get_sudoku_quadrant(fixed_mask, quadrant_no)
        counter = Counter(quadrant_fixed_mask)
        if "0" in counter and counter["0"] >= 2:
            swappable.append(quadrant_no)
    if not swappable:
        raise ValueError("There is no quadrant with at least two swappable numbers.")
    return swappable


def sudoku_cost_function(sudoku: str) -> (int, List[int], List[int]):
    length = assert_sudoku_is_valid_and_get_length(sudoku)
    costs_per_line = [
        count_duplicates(get_sudoku_line(sudoku, i)) for i in range(length)
    ]
    costs_per_row = [count_duplicates(get_sudoku_row(sudoku, j)) for j in range(length)]
    return (
        sum(costs_per_line + costs_per_row),
        costs_per_line,
        costs_per_row,
    )


def sudoku_random_swap(sudoku: str, fixed_mask: str) -> str:
    swappable_quadrants = get_swappable_quadrants(fixed_mask)
    quadrant_no = choice(swappable_quadrants)
    quadrant = get_sudoku_quadrant(sudoku, quadrant_no)
    quadrant_fixed_mask = get_sudoku_quadrant(fixed_mask, quadrant_no)
    swap_candidates = [i for i, value in enumerate(quadrant_fixed_mask) if value == "0"]
    swap_a, swap_b = sorted(sample(swap_candidates, k=2))
    quadrant_after_swap = (
        quadrant[:swap_a]
        + quadrant[swap_b]
        + quadrant[swap_a + 1 : swap_b]
        + quadrant[swap_a]
        + quadrant[swap_b + 1 :]
    )
    return sudoku_replace_quadrant(sudoku, quadrant_no, quadrant_after_swap)
