from math import exp
from random import random
from statistics import pstdev
from time import sleep
from typing import Callable, List

from src.sudoku_annealing.sudoku import (
    get_swappable_quadrants,
    sudoku_cost_function,
    sudoku_random_swap,
)
from sudoku import (
    sudoku_quadrant_valid_fill,
    sudoku_replace_quadrant,
    get_sudoku_quadrant,
    get_sudoku_fixed_mask,
)


def simulated_annealing(
    sudoku: str,
    alpha: float,
    update_status: Callable[[str], None],
    update_sudoku_plot: Callable[[str, str], None],
    update_costs_plot: Callable[[List[float]], None],
    update_temperature_plot: Callable[[List[float]], None],
) -> None:
    fixed_mask = get_sudoku_fixed_mask(sudoku)

    update_status("Finding start configuration")
    for quadrant_no in range(9):
        quadrant = get_sudoku_quadrant(sudoku, quadrant_no)
        filled_quadrant = sudoku_quadrant_valid_fill(quadrant)
        sudoku = sudoku_replace_quadrant(sudoku, quadrant_no, filled_quadrant)
    update_sudoku_plot(sudoku, fixed_mask)

    try:
        get_swappable_quadrants(fixed_mask)
    except ValueError:
        if sudoku_cost_function(sudoku)[0] == 0:
            update_status("Found optimal solution")
        else:
            update_status("Sudoku has no valid solution")

    update_status("Finding initial temperature")
    sleep(1.0)
    initial_temperature = pstdev(  # according to Lewis
        sudoku_cost_function(sudoku_random_swap(sudoku, fixed_mask))[0]
        for _ in range(1000)
    )

    update_status(f"Initial temperature is {initial_temperature:.2}")
    sleep(1.0)

    update_status(f"Start simulated annealing")
    temperature = initial_temperature
    cost = sudoku_cost_function(sudoku)[0]

    costs = []
    temperatures = []
    for i in range(100000):
        proposed_change = sudoku_random_swap(sudoku, fixed_mask)
        proposed_cost = sudoku_cost_function(proposed_change)[0]
        if proposed_cost <= cost:
            accept = True
        else:
            accept_probability = exp(-abs(proposed_cost - cost) / temperature)
            accept = random() < accept_probability

        if accept:
            sudoku = proposed_change
            cost = proposed_cost

        costs.append(cost)
        temperatures.append(temperature)
        if i == 1 or i % 20 == 0 or cost == 0:
            update_sudoku_plot(sudoku, fixed_mask)
            update_costs_plot(costs)
            update_temperature_plot(temperatures)

        temperature = alpha * temperature
        if (
            cost > 0 and len(costs) > 2500 and len(set(costs[-2000:])) == 1
        ):  # constant cost function
            update_status("Reheated the system")
            temperature = initial_temperature
        if cost == 0:
            break

    if cost == 0:
        update_status("Found solution")
    else:
        update_status(
            "Simulated annealing did not converge within computational budget"
        )
