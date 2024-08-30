from matplotlib import pyplot as plt

# This file is mostly powered by ChatGPT-4o


def plot_sudoku(
    sudoku_string, fixed_string, costs_per_row, costs_per_column, total_cost, ax
):
    # Parse the Sudoku string into a 9x9 grid
    rows = sudoku_string.strip().split("\n")
    grid = [[int(char) if char.isdigit() else 0 for char in row] for row in rows]

    # Parse the fixed string into a 9x9 grid of flags
    fixed_rows = fixed_string.strip().split("\n")
    fixed_grid = [
        [int(char) if char in "01" else 0 for char in row] for row in fixed_rows
    ]

    # Clear previous plot
    ax.clear()

    # Set the aspect of the plot to be equal
    ax.set_aspect("equal")

    # Draw the grid
    ax.set_xticks([i - 0.5 for i in range(1, 9)], minor=True)
    ax.set_yticks([i - 0.5 for i in range(1, 9)], minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=3)

    # Set limits and turn off ticks
    ax.set_xlim(-0.5, 11.5)  # Extend x-axis for column scores
    ax.set_ylim(10.5, -2.5)  # Extend y-axis for row scores and total cost
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Fill in the numbers with appropriate styles
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Check if the number is fixed or not
                if fixed_grid[i][j] == 1:
                    # Bold and black for fixed numbers
                    ax.text(
                        j,
                        i,
                        str(grid[i][j]),
                        ha="center",
                        va="center",
                        fontsize=16,
                        color="black",
                        fontweight="bold",
                    )
                else:
                    # Non-bold and dark green for non-fixed numbers
                    ax.text(
                        j,
                        i,
                        str(grid[i][j]),
                        ha="center",
                        va="center",
                        fontsize=16,
                        color="#006400",
                    )

    # Highlight the 3x3 sub-grids
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            ax.add_patch(
                plt.Rectangle(
                    (j - 0.5, i - 0.5), 3, 3, fill=False, edgecolor="black", lw=3
                )
            )

    # Add row scores on the right side, connected and without rounded edges
    for i, cost in enumerate(costs_per_row):
        ax.add_patch(
            plt.Rectangle(
                (9.5, i - 0.5), 1, 1, fill=True, color="lightblue", edgecolor="black"
            )
        )
        ax.text(10, i, str(cost), ha="center", va="center", fontsize=12, color="blue")

    # Add dividing lines between every three rows in the row scores
    # for i in range(0, 9, 3):
    #     ax.plot([9.5, 10.5], [i - 0.5, i - 0.5], color="black", linewidth=3)

    # Add column scores below the grid, connected and without rounded edges
    for j, cost in enumerate(costs_per_column):
        ax.add_patch(
            plt.Rectangle(
                (j - 0.5, 9.5), 1, 1, fill=True, color="lightblue", edgecolor="black"
            )
        )
        ax.text(j, 10, str(cost), ha="center", va="center", fontsize=12, color="blue")

    # Add dividing lines between every three columns in the column scores
    # for j in range(0, 9, 3):
    #     ax.plot([j - 0.5, j + 0.5], [9.5, 9.5], color="black", linewidth=3)

    # Add total cost below the grid, without connection to the row/column scores
    ax.text(
        10, 10, str(total_cost), ha="center", va="center", fontsize=14, color="black"
    )
    ax.text(10, 11, "Total Cost", ha="center", va="center", fontsize=10, color="black")

    ax.set_title("Sudoku Solver")
    ax.axis("off")  # Hide axes
