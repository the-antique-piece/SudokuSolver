"""
this is the main module.
"""

import tkinter as tk
from gui.sudoku_gui import SudokuSolverGUI


def main():
    """
    entery point for the app
    """
    root = tk.Tk()
    SudokuSolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
