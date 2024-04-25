"""
this is the maine module.
"""

import tkinter as tk
from gui.sudoku_gui import SudokuSolverGUI


def main():
    """
    entery point for the app
    """
    root = tk.Tk()
    gui = SudokuSolverGUI(root)
    # Bind the window close event to the close_application function
    root.protocol("WM_DELETE_WINDOW", gui.close_application)
    root.mainloop()


if __name__ == "__main__":
    main()
