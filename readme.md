# Simulated Annealing Sudoku Solver
This is a quick implementation of a [paper](https://link.springer.com/content/pdf/10.1007/s10732-007-9012-8.pdf) by Rhyd Lewis. 
It finds the global optimum (aka the solution) of a Sudoku puzzle using simulated annealing.

I implemented with a short time budget and the computation is not optimized.
What is great about it, though, is that you can watch the algorithm solve the Sudoku puzzle in real time.

## Preview

https://github.com/manolo-lolo/sudoku-simulated-annealing/raw/main/videos/solver.webm.mov

## Reheating
Sometimes the system will get stuck close to a non-global optimum (aka not the solution). In that case, the system is automatically reheated.

https://github.com/manolo-lolo/sudoku-simulated-annealing/raw/main/videos/reheat.webm.mov


## Requirements
Python 3.10, Tkinter, Poetry
```bash
sudo apt install python3 python3-tk python3-poetry
poetry install
```
