"""
test cases for SudokuSolverGUI
"""
import tkinter as tk
from tkinter import Tk
import unittest
from unittest.mock import MagicMock, patch
from src.sudoku_solver import SudokuSolverLogic
from gui.sudoku_gui import SudokuSolverGUI


class TestSudokuSolverGUI(unittest.TestCase):
    """
    TestSudokuSolverGUI class
    """

    def setUp(self):
        self.root = Tk()
        self.gui = SudokuSolverGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_create_grid(self):
        """
        test create grid method
        """
        self.assertEqual(len(self.gui.puzzle), 9)
        for row in self.gui.puzzle:
            self.assertEqual(len(row), 9)
            for entry in row:
                self.assertIsInstance(entry, tk.StringVar)

    def test_solve_button_click(self):
        """
        test is solve_button clicked
        """
        # Mock the solve method
        self.gui.solve = MagicMock()

        # Simulate button click
        self.gui.solve_button.event_generate("<<Button-1>>")

        # Verify that the solve method was called
        self.gui.solve.assert_called_once()

    def test_clear_button_click(self):
        """
        test clear button is clicked
        """
        self.gui.clear = MagicMock()
        # Simulate button click
        self.gui.clear_button.event_generate("<<Button-1>>")
        self.gui.clear.assert_called_once()

    def test_validate_input_valid(self):
        """
        validate input
        """
        valid_input = "5"
        self.assertTrue(self.gui.validate_input(valid_input))

    def test_validate_input_invalid(self):
        """
        checks invalid input
        """
        invalid_inputs = ["", "a", "0", "10"]
        for input_value in invalid_inputs:
            self.assertFalse(self.gui.validate_input(input_value))

    def test_check_duplicates_no_duplicates(self):
        """
        checks for duplicate values
        """
        self.assertTrue(self.gui.check_duplicates())

    def test_check_duplicates_with_duplicates(self):
        """
        duplicate
        """
        self.gui.puzzle[0][0].set("1")
        self.gui.puzzle[1][0].set("1")
        self.assertFalse(self.gui.check_duplicates())

    def test_solve_with_solution(self):
        """
        test the solution
        """
        # Mock the SudokuSolverLogic.solve_sudoku method
        SudokuSolverLogic.solve_sudoku = MagicMock(return_value=[[1]*9]*9)
        self.gui.solve()
        # Check if the puzzle grid is updated with the solution
        for i in range(9):
            for j in range(9):
                self.assertEqual(self.gui.puzzle[i][j].get(), "1")

    def test_solve_without_solution(self):
        """ 
        no solution
        """
        with patch('gui.sudoku_gui.messagebox.showinfo') as mock_showinfo:
            # Mock the SudokuSolverLogic.solve_sudoku method to return None
            SudokuSolverLogic.solve_sudoku = MagicMock(return_value=None)
            self.gui.solve()
            # Check if a warning message is displayed
            mock_showinfo.assert_called_once()

    def test_clear(self):
        """
        clear the grid
        """
        for i in range(9):
            for j in range(9):
                self.gui.puzzle[i][j].set("1")
        self.gui.clear()
        for i in range(9):
            for j in range(9):
                self.assertEqual(self.gui.puzzle[i][j].get(), "")


if __name__ == "__main__":
    unittest.main()
