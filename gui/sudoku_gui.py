"""
tkinter lib imported for creating gui
"""
import tkinter as tk
from tkinter import messagebox
from src.sudoku_solver import solve_sudoku  # Import the Sudoku solver function


class SudokuSolverGUI:
    """
    This is the class for Sudoku GUI Design
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")

        self.puzzle = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

        self.create_grid()

        solve_button = tk.Button(
            self.master, text="Solve", command=self.solve, bg="lightgreen", width=8,
            font=("Elephant", 30, "bold"))
        solve_button.grid(row=9, column=1, columnspan=4, pady=20)

        clear_button = tk.Button(
            self.master, text="Clear", command=self.clear, bg="lightcoral", width=8,
            font=("Copper Black", 30, "bold"))
        clear_button.grid(row=9, column=4, columnspan=8, pady=20)

    def create_grid(self):
        """
        creates 9x9 grids
        """
        color_scheme = {
            (0, 0): "lightblue", (0, 1): "lightblue", (0, 2): "lightblue",
            (1, 0): "lightblue", (1, 1): "lightblue", (1, 2): "lightblue",
            (2, 0): "lightblue", (2, 1): "lightblue", (2, 2): "lightblue",
            (0, 3): "lightgreen", (0, 4): "lightgreen", (0, 5): "lightgreen",
            (1, 3): "lightgreen", (1, 4): "lightgreen", (1, 5): "lightgreen",
            (2, 3): "lightgreen", (2, 4): "lightgreen", (2, 5): "lightgreen",
            (0, 6): "lightcoral", (0, 7): "lightcoral", (0, 8): "lightcoral",
            (1, 6): "lightcoral", (1, 7): "lightcoral", (1, 8): "lightcoral",
            (2, 6): "lightcoral", (2, 7): "lightcoral", (2, 8): "lightcoral",
            (3, 0): "lightgreen", (3, 1): "lightgreen", (3, 2): "lightgreen",
            (4, 0): "lightgreen", (4, 1): "lightgreen", (4, 2): "lightgreen",
            (5, 0): "lightgreen", (5, 1): "lightgreen", (5, 2): "lightgreen",
            (3, 3): "lightcoral", (3, 4): "lightcoral", (3, 5): "lightcoral",
            (4, 3): "lightcoral", (4, 4): "lightcoral", (4, 5): "lightcoral",
            (5, 3): "lightcoral", (5, 4): "lightcoral", (5, 5): "lightcoral",
            (3, 6): "lightblue", (3, 7): "lightblue", (3, 8): "lightblue",
            (4, 6): "lightblue", (4, 7): "lightblue", (4, 8): "lightblue",
            (5, 6): "lightblue", (5, 7): "lightblue", (5, 8): "lightblue",
            (6, 0): "lightcoral", (6, 1): "lightcoral", (6, 2): "lightcoral",
            (7, 0): "lightcoral", (7, 1): "lightcoral", (7, 2): "lightcoral",
            (8, 0): "lightcoral", (8, 1): "lightcoral", (8, 2): "lightcoral",
            (6, 3): "lightblue", (6, 4): "lightblue", (6, 5): "lightblue",
            (7, 3): "lightblue", (7, 4): "lightblue", (7, 5): "lightblue",
            (8, 3): "lightblue", (8, 4): "lightblue", (8, 5): "lightblue",
            (6, 6): "lightgreen", (6, 7): "lightgreen", (6, 8): "lightgreen",
            (7, 6): "lightgreen", (7, 7): "lightgreen", (7, 8): "lightgreen",
            (8, 6): "lightgreen", (8, 7): "lightgreen", (8, 8): "lightgreen",
        }

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(
                    self.master, width=5,
                    textvariable=self.puzzle[i][j], bg=color_scheme.get((i, j), "white"))
                entry.grid(row=i, column=j)
                entry.config(font=('Monoscaped', 44))
                entry.config(validate="key")
                entry.config(validatecommand=(
                    entry.register(self.validate_input), "%P"))
                entry.config(justify="center")

    def validate_input(self, value):
        """
        Validate user input to ensure only numbers from 1 to 9 are allowed
        """
        if value.isdigit() and 1 <= int(value) <= 9:
            return True
        else:
            return False

    def check_duplicates(self):
        """
        Check for duplicate values in rows, columns, and 3x3 grids
        """
        for i in range(9):
            row_values = set()
            col_values = set()
            grid_values = set()
            for j in range(9):
                row_value = self.puzzle[i][j].get()
                col_value = self.puzzle[j][i].get()
                grid_row = 3 * (i // 3) + j // 3
                grid_col = 3 * (i % 3) + j % 3
                grid_value = self.puzzle[grid_row][grid_col].get()

                if row_value != "" and row_value in row_values:
                    return False
                if col_value != "" and col_value in col_values:
                    return False
                if grid_value != "" and grid_value in grid_values:
                    return False

                row_values.add(row_value)
                col_values.add(col_value)
                grid_values.add(grid_value)

        return True

    def solve(self):
        """
        Solve the Sudoku puzzle
        """
        # Check for duplicate values before solving the puzzle
        if not self.check_duplicates():
            messagebox.showinfo(
                "No Solution! No Solution exists for the provided puzzle.")
            return

        # Convert the puzzle grid to a 2D list
        sudoku_grid = [[0 if var.get() == "" else int(var.get())
                        for var in row] for row in self.puzzle]

        # Solve the Sudoku puzzle
        solution = solve_sudoku(sudoku_grid)

        # Check if a solution is found
        if solution is not None:
            # Update the puzzle grid with the solution
            for i in range(9):
                for j in range(9):
                    self.puzzle[i][j].set(solution[i][j])
        else:
            # Display a message indicating that no solution exists
            message = """No Solution", "No solution exists for the provided puzzle.
            Reason: The Puzzle contains duplicate values in either rows, 
            columns, or 3x3 subgrids."""
            messagebox.showinfo("No Solution", message,
                                icon='warning', width=600, height=200)

    def clear(self):
        """
        Clears all entries in the puzzle
        """
        for i in range(9):
            for j in range(9):
                self.puzzle[i][j].set("")
