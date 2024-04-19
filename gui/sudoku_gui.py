"""
resource_path()
"""
import sys
import os
import tkinter as tk
from src.sudoku_solver import SudokuSolverLogic


class SudokuSolverGUI:
    """
    class to encapsulate all the things in a place
    """

    def resource_path(self, relative_path):
        """
        Get absolute path to resource, works for dev and for PyInstaller.
        """
        if hasattr(sys, '_MEI259162'):
            return os.path.join(sys._MEI259162, relative_path)    # pylint: disable=protected-access

        return os.path.abspath(relative_path)


# Use resource_path to get the correct icon path

    def __init__(self, master):
        """
        initialize the views
        """
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.geometry("1200x600")
        icon_path = self.resource_path(
            r"icons\sudoku-icon.ico")
        # Use the icon path in the GUI initialization
        self.master.iconbitmap(icon_path)
        greeting_label = tk.Label(self.master, text="Hey Buddy! Welcome to Sudoku World.", font=(
            "Copper Black", 20, "bold"), fg="purple")
        greeting_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")

        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.grid(row=1, column=0, pady=(
            0, 10), padx=(20, 20), sticky="nsew")

        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")

        self.puzzle = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

        self.create_grid()
        self.create_buttons()

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_grid(self):
        """
        create the grid
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
                    self.grid_frame, textvariable=self.puzzle[i][j],
                    bg=color_scheme.get((i, j), "white"))
                entry.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                entry.config(font=('Monoscaped', 30))
                entry.config(validate="key", validatecommand=(
                    entry.register(self.validate_input), "%P"))
                entry.config(justify="center")

                # Bind the KeyRelease event to each entry
                entry.bind("<KeyRelease>", lambda event, row=i,
                           col=j: self.move_to_next_cell(row, col))
                # Bind the arrow keys to move the focus
                # Bind the arrow keys to move the focus
                entry.bind("<Left>", lambda event, row=i,
                           col=j: self.move_focus(event, row, col, 0, -1))
                entry.bind("<Right>", lambda event, row=i,
                           col=j: self.move_focus(event, row, col, 0, 1))
                entry.bind("<Up>", lambda event, row=i,
                           col=j: self.move_focus(event, row, col, -1, 0))
                entry.bind("<Down>", lambda event, row=i,
                           col=j: self.move_focus(event, row, col, 1, 0))

                self.grid_frame.grid_columnconfigure(j, weight=1)
                self.grid_frame.grid_rowconfigure(i, weight=1)

    def move_focus(self, event, row, col, row_offset, col_offset):
        # pylint: disable=unused-argument
        """
        Move the focus to the adjacent cell based on the arrow key pressed
        """
        # The 'event' parameter is not used in this method, so we can remove it
        next_row = row + row_offset
        next_col = col + col_offset

        # Check if the next cell is within the grid boundaries
        if 0 <= next_row < 9 and 0 <= next_col < 9:
            next_entry = self.grid_frame.grid_slaves(
                row=next_row, column=next_col)[0]
            next_entry.focus_set()  # Move the focus to the next entry

    def move_to_next_cell(self, row, col):
        """
        Move the cursor to the next cell when a key is released
        """
        # Get the input value
        value = self.puzzle[row][col].get()

        # Check if the input is valid (a single digit)
        if value.isdigit() and 1 <= int(value) <= 9:
            # Replace the previous value with the new one
            self.puzzle[row][col].set(value)

            # Move the cursor to the next cell if it's not in the last column
            if col < 8:
                next_entry = self.grid_frame.grid_slaves(
                    row=row, column=col + 1)[0]
                next_entry.focus_set()  # Move the focus to the next entry
            # Move the cursor to the first cell of the next row if it's in the last column
            elif row < 8:
                next_entry = self.grid_frame.grid_slaves(
                    row=row + 1, column=0)[0]
                next_entry.focus_set()  # Move the focus to the next entry

    def create_buttons(self):
        """
        creates  buttons
        """
        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve,
                                      bg="lightgreen", width=6, font=("Copper Black", 26, "bold"))
        self.solve_button.grid(row=0, column=0, padx=(160, 0))

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear,
                                      bg="lightcoral", width=6, font=("Copper Black", 26, "bold"))
        self.clear_button.grid(row=0, column=0, padx=(630, 0))

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def validate_input(self, value):
        """
        Validate user input to ensure only numbers from 1 to 9 are allowed
        """
        if value == "":
            return True  # Allow empty cells to be edited
        elif value.isdigit() and 1 <= int(value) <= 9:
            return True  # Validate input for non-empty cells
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
            message = """No solution exists for the provided puzzle.
            \n\nReason: The puzzle contains duplicate values in either rows,columns, or 3x3 subgrids.
            \nPlease correct the duplicates and try again."""
            self.show_detailed_message(message)
            return

        # Convert the puzzle grid to a 2D list
        sudoku_grid = [[0 if var.get() == "" else int(var.get())
                        for var in row] for row in self.puzzle]

        # Solve the Sudoku puzzle
        solution = SudokuSolverLogic.solve_sudoku(sudoku_grid)

        # Check if a solution is found
        if solution is not None:
            # Update the puzzle grid with the solution
            for i in range(9):
                for j in range(9):
                    self.puzzle[i][j].set(solution[i][j])

    def show_detailed_message(self, message):
        """
        Display a detailed message using a custom dialog with resizable text.
        """
        dialog = tk.Toplevel()
        dialog.title("No Solution!")
        dialog.geometry("400x200")  # Set initial size of the dialog
        icon_path = self.resource_path(r"icons\sudoku-icon.ico")
        dialog.iconbitmap(icon_path)
        text = tk.Text(dialog, wrap="word", height=10, width=40)
        text.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure a tag for left alignment
        text.tag_configure("left", justify="left")
        # Apply the "left" tag to the inserted text
        text.insert("1.0", message, "left")
        text.config(state="disabled")

        # Allow the user to resize the dialog
        dialog.resizable(True, True)

        dialog.transient()  # Set dialog as transient to the main window
        dialog.grab_set()   # Grab focus to the dialog
        dialog.focus_set()  # Set focus to the dialog
        dialog.wait_window()  # Wait for the dialog to be closed

    def clear(self):
        """
        Clears all entries in the puzzle
        """
        for i in range(9):
            for j in range(9):
                self.puzzle[i][j].set("")
                # Ensure that the cleared entries are validated
                entry = self.grid_frame.grid_slaves(row=i, column=j)[0]
                entry.config(validate="key", validatecommand=(
                    entry.register(self.validate_input), "%P"))
