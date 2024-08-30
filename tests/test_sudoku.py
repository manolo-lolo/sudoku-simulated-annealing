from random import seed

from src.sudoku_annealing.sudoku import (
    count_duplicates,
    assert_sudoku_is_valid_and_get_length,
    get_sudoku_line,
    get_sudoku_row,
    get_sudoku_quadrant,
    sudoku_cost_function,
    get_sudoku_fixed_mask,
    sudoku_quadrant_valid_fill,
    sudoku_replace_quadrant,
    get_swappable_quadrants,
    sudoku_random_swap,
)
import pytest

small_test_sudoku = """
1234
2341
3412
4321
""".strip()

normal_test_sudoku = """
123456789
234567891
345678912
456789123
567891234
678912345
789123456
891234567
912345678
""".strip()

replacement_quadrant = """
951
367
214
""".strip()


@pytest.mark.parametrize(
    "sequence, expected",
    (
        ("00000", 0),
        ("00123", 0),
        ("00112", 1),
        ("02112", 2),
        ("10001", 1),
        ("11001", 2),
        ("11221", 3),
        ("11121", 3),
        ("11111", 4),
        ("1230123", 3),
    ),
)
def test_count_duplicates(sequence: str, expected: int):
    assert count_duplicates(sequence) == expected


@pytest.mark.parametrize(
    "sudoku",
    (
        """""",
        """\n""",
        """123""",
        """123\n""",
        """123\n\n""",
        """123\n12\n123""",
        """12\n123\n123""",
        """123\n123\n12""",
        """123123123""",
        """123\n123123""",
    ),
)
def test_assert_sudoku_is_valid_and_get_length_for_invalid(sudoku: str):
    with pytest.raises(ValueError):
        assert_sudoku_is_valid_and_get_length(sudoku)


@pytest.mark.parametrize(
    "sudoku, sudoku_length",
    (
        ("""1""", 1),
        ("""12\n21""", 2),
        ("""123\n123\n123""", 3),
        ("""123\n123\n321""", 3),
        ("""1234\n1234\n3214\n4321""", 4),
        ("""000\n000\n000""", 3),
    ),
)
def test_assert_sudoku_is_valid_and_get_length_for_valid(sudoku: str, sudoku_length: int):
    assert assert_sudoku_is_valid_and_get_length(sudoku) == sudoku_length


@pytest.mark.parametrize("line_no, expected", ((0, "1234"), (1, "2341"), (2, "3412"), (3, "4321")))
def test_get_sudoku_line(line_no, expected):
    assert get_sudoku_line(small_test_sudoku, line_no) == expected


@pytest.mark.parametrize("row_no, expected", ((0, "1234"), (1, "2343"), (2, "3412"), (3, "4121")))
def test_get_sudoku_row(row_no, expected):
    assert get_sudoku_row(small_test_sudoku, row_no) == expected


@pytest.mark.parametrize(
    "quadrant_no, expected",
    (
        (0, "123\n234\n345"),
        (2, "789\n891\n912"),
        (4, "789\n891\n912"),
        (8, "456\n567\n678"),
    ),
)
def test_get_sudoku_quadrant(quadrant_no, expected):
    assert get_sudoku_quadrant(normal_test_sudoku, quadrant_no) == expected


@pytest.mark.parametrize(
    "sudoku, expected_cost",
    (
        ("1", 0),
        ("00\n12", 0),
        ("21\n12", 0),
        ("02\n12", 1),
        ("12\n12", 2),
        ("123\n231\n312", 0),
        ("123\n100\n312", 1),
        ("123\n100\n132", 2),
        ("111\n000\n000", 2),
        ("111\n220\n000", 3),
        ("111\n222\n000", 4),
        ("111\n111\n111", 12),
    ),
)
def test_sudoku_cost_function(sudoku: str, expected_cost: int):
    assert sudoku_cost_function(sudoku)[0] == expected_cost
    # fixme the other two values are not tested yet


@pytest.mark.parametrize(
    "sudoku, expected_mask",
    (
        ("0", "0"),
        ("5", "1"),
        ("12\n00", "11\n00"),
        ("10\n50", "10\n10"),
        ("023\n103\n120", "011\n101\n110"),
    ),
)
def test_get_sudoku_fixed_mask(sudoku: str, expected_mask: str):
    assert get_sudoku_fixed_mask(sudoku) == expected_mask


@pytest.mark.parametrize(
    "quadrant", ("123\n456\n789", "123\n456\n780", "103\n406\n000", "000\n000\n000")
)
def test_sudoku_quadrant_valid_fill(quadrant):
    seed(31415926535897932385)
    assert assert_sudoku_is_valid_and_get_length(quadrant) == 3
    for _ in range(100):
        filled_quadrant = sudoku_quadrant_valid_fill(quadrant)
        assert assert_sudoku_is_valid_and_get_length(filled_quadrant) == 3
        assert set(filled_quadrant) == {"1", "2", "3", "4", "5", "6", "7", "8", "9", "\n"}
        for i in range(3):
            for j in range(3):
                original = get_sudoku_line(quadrant, i)[j]
                altered = get_sudoku_line(filled_quadrant, i)[j]
                if original != "0":
                    assert original == altered


@pytest.mark.parametrize(
    "quadrant_no, expected",
    (
        (
            0,
            """
951456789
367567891
214678912
456789123
567891234
678912345
789123456
891234567
912345678
""",
        ),
        (
            1,
            """
123951789
234367891
345214912
456789123
567891234
678912345
789123456
891234567
912345678
""",
        ),
        (
            3,
            """
123456789
234567891
345678912
951789123
367891234
214912345
789123456
891234567
912345678
""",
        ),
        (
            8,
            """
123456789
234567891
345678912
456789123
567891234
678912345
789123951
891234367
912345214
""",
        ),
    ),
)
def test_sudoku_replace_quadrant(quadrant_no: int, expected: str):
    assert (
        sudoku_replace_quadrant(normal_test_sudoku, quadrant_no, replacement_quadrant.strip())
        == expected.strip()
    )


@pytest.mark.parametrize(
    "fixed_mask, ground_truth_swappable",
    (
        (
            """
111111111
111011101
111101111
111111111
111111111
111111111
111111111
111111111
111011101
""",
            [1],
        ),
        (
            """
101111111
101111101
100101111
111111111
111111111
111111111
111111101
111111101
111011101
""",
            [0, 8],
        ),
        (
            """
111111111
111111101
111101111
111111111
111111101
101111111
111111111
111111111
111011101
""",
            [],
        ),
    ),
)
def test_assert_exists_swappable_quadrant(fixed_mask: str, ground_truth_swappable):
    if ground_truth_swappable:
        assert get_swappable_quadrants(fixed_mask.strip()) == ground_truth_swappable
    else:
        with pytest.raises(ValueError):
            get_swappable_quadrants(fixed_mask.strip())


def test_sudoku_random_swap_basic_test():
    trivial_fixed_mask = """
111111101
111111101
111111111
111111111
111111111
111111111
111111111
111111111
111111111
""".strip()
    assert (
        sudoku_random_swap(normal_test_sudoku, trivial_fixed_mask)
        == """
123456799
234567881
345678912
456789123
567891234
678912345
789123456
891234567
912345678
""".strip()
    )

    realistic_fixed_mask = """
101101101
101101101
101101010
111011110
101111110
101011110
111011010
111101010
111111111
    """.strip()
    seed(3141592653589793238)
    for _ in range(50):
        swapped_sudoku = sudoku_random_swap(normal_test_sudoku, realistic_fixed_mask)
        assert len(normal_test_sudoku) == len(realistic_fixed_mask) == len(swapped_sudoku)
        assert swapped_sudoku != normal_test_sudoku
        for original, mask, swapped in zip(
            normal_test_sudoku, realistic_fixed_mask, swapped_sudoku
        ):
            if mask in {"1", "\n"}:
                assert original == swapped
