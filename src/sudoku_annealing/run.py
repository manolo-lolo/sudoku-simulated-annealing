import tkinter as tk
from math import ceil
from typing import List

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from data import normal_1
from src.sudoku_annealing.plot import plot_sudoku
from src.sudoku_annealing.simulated_annealing import simulated_annealing
from src.sudoku_annealing.sudoku import sudoku_cost_function, get_sudoku_fixed_mask

# This file is mostly powered by ChatGPT-4o


# Step 1: Create the main application window
root = tk.Tk()
root.title("Sudoku Solver")
root.configure(bg="white")

# Create the main frame that will contain the Sudoku and plots side by side
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the left frame for the Sudoku grid
left_frame = tk.Frame(main_frame, bg="white")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the right frame for the plots (cost function and temperature)
right_frame = tk.Frame(main_frame, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create the top frame within the right frame for the cost function plot
top_right_frame = tk.Frame(right_frame, bg="white")
top_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the bottom frame within the right frame for the temperature plot
bottom_right_frame = tk.Frame(right_frame, bg="white")
bottom_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame below the plots for the parameter input, status, and button
control_frame = tk.Frame(right_frame, bg="white")
control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Step 2: Add a placeholder for the Sudoku plot
fig_sudoku = Figure(figsize=(5, 5), dpi=100)
ax_sudoku = fig_sudoku.add_subplot(111)

# Add the Sudoku plot to the left frame
canvas_sudoku = FigureCanvasTkAgg(fig_sudoku, master=left_frame)
canvas_sudoku.draw()
canvas_sudoku.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Step 3: Add a placeholder for the cost function plot
fig_cost = Figure(figsize=(5, 2.5), dpi=100)
ax_cost = fig_cost.add_subplot(111)
ax_cost.set_title("Cost Function")

# Add the cost function plot to the top right frame
canvas_cost = FigureCanvasTkAgg(fig_cost, master=top_right_frame)
canvas_cost.draw()
canvas_cost.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Step 4: Add a placeholder for the temperature plot
fig_temp = Figure(figsize=(5, 2.5), dpi=100)
ax_temp = fig_temp.add_subplot(111)
ax_temp.set_title("Temperature")

# Add the temperature plot to the bottom right frame
canvas_temp = FigureCanvasTkAgg(fig_temp, master=bottom_right_frame)
canvas_temp.draw()
canvas_temp.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Step 5: Add parameter input for alpha, status text, and start button
# Label for alpha input
alpha_label = tk.Label(control_frame, text="Alpha:", bg="white")
alpha_label.pack(side=tk.LEFT)

# Entry for alpha input, pre-set to 0.99
alpha_entry = tk.Entry(control_frame)
alpha_entry.insert(0, "0.99")
alpha_entry.pack(side=tk.LEFT, padx=5)

# Status text field
status_label = tk.Label(control_frame, text="Status:", bg="white")
status_label.pack(side=tk.LEFT, padx=(10, 5))
status_text = tk.StringVar()
status_entry = tk.Entry(
    control_frame, textvariable=status_text, state="readonly", width=30
)
status_entry.pack(side=tk.LEFT)

# Start button
start_button = tk.Button(
    control_frame,
    text="Start",
    bg="#4CAF50",
    fg="white",
    command=lambda: start_solving(float(alpha_entry.get())),
)
start_button.pack(side=tk.LEFT, padx=10)


def start_solving(alpha: float):
    simulated_annealing(
        normal_1,
        alpha,
        update_status,
        update_sudoku_plot,
        update_costs_plot,
        update_temperature_plot,
    )


def update_sudoku_plot(sudoku_string: str, fixed_string: str):
    """Updates the Sudoku plot with a new Sudoku string."""
    total_cost, costs_per_row, costs_per_column = sudoku_cost_function(sudoku_string)
    plot_sudoku(
        sudoku_string,
        fixed_string,
        costs_per_row,
        costs_per_column,
        total_cost,
        ax_sudoku,
    )
    canvas_sudoku.draw()  # Redraw the canvas to display the updated plot
    root.update_idletasks()  # Refresh UI
    root.update()


def update_status(status: str):
    """Updates the status text field."""
    status_text.set(status)
    root.update_idletasks()  # Refresh UI
    root.update()


def update_costs_plot(costs: List[float]):
    """Updates the cost function plot."""
    ax_cost.clear()
    ax_cost.plot(costs, color="blue")
    ax_cost.set_title("Cost Function")
    ax_cost.set_xlabel("Time Step")
    ax_cost.set_xlim(right=ceil(len(costs) / 1000) * 1000)
    ax_cost.set_ylabel("Cost")
    ax_cost.set_ylim([0, 50])
    canvas_cost.draw()
    root.update_idletasks()  # Refresh UI
    root.update()


def update_temperature_plot(temperatures: List[float]):
    """Updates the temperature plot."""
    ax_temp.clear()
    ax_temp.plot(temperatures, color="red")
    ax_temp.set_title("Temperature")
    ax_temp.set_xlabel("Time Step")
    ax_temp.set_xlim(right=ceil(len(temperatures) / 1000) * 1000)
    ax_temp.set_ylabel("Temperature")
    ax_temp.set_ylim([0.0, 1.8])
    canvas_temp.draw()
    root.update_idletasks()  # Refresh UI
    root.update()


# Print unsolved Sudoku at startup
update_sudoku_plot(normal_1, get_sudoku_fixed_mask(normal_1))


# Run the Tkinter main loop
root.mainloop()
