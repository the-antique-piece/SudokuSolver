"""Module for testing gui"""
import unittest
from unittest.mock import MagicMock, patch
import os
from tkinter import Tk, StringVar, Entry
from src.sudoku_solver import SudokuSolverLogic
from gui.sudoku_gui import SudokuSolverGUI


class TestSudokuSolverGUI(unittest.TestCase):
    """ Class for testing SudokuSolverGUI class"""

    def setUp(self):
        self.master = Tk()  # Create a Tk instance
        self.gui = SudokuSolverGUI(self.master)

    def test_validate_input(self):
        """Test valid inputs"""
        self.assertTrue(self.gui.validate_input("1"))
        self.assertTrue(self.gui.validate_input("9"))
        # Test invalid inputs
        self.assertFalse(self.gui.validate_input("0"))
        self.assertFalse(self.gui.validate_input("10"))
        self.assertFalse(self.gui.validate_input("a"))
        self.assertFalse(self.gui.validate_input("!"))
        # Handles missing 'master' argument.

    def test_solve(self):
        """Test solving a valid puzzle"""
        valid_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.gui.puzzle = [[StringVar(
            value=str(cell) if cell != 0 else "") for cell in row] for row in valid_puzzle]
        self.gui.solve()
        solved_puzzle = [[cell.get() for cell in row]
                         for row in self.gui.puzzle]
        self.assertTrue(SudokuSolverLogic.solve_sudoku(
            valid_puzzle) == solved_puzzle)

        # Test solving an invalid puzzle
        invalid_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 5]  # Invalid last cell
        ]
        self.gui.puzzle = [[StringVar(value=str(
            cell) if cell != 0 else "") for cell in row] for row in invalid_puzzle]
        self.gui.solve()
        solved_puzzle = [[cell.get() for cell in row]
                         for row in self.gui.puzzle]
        self.assertFalse(SudokuSolverLogic.solve_sudoku(
            invalid_puzzle) == solved_puzzle)

    def test_move_to_next_cell(self):
        """Test moving to the next cell within the same row"""
        self.gui.move_to_next_cell(0, 0)
        self.assertTrue(self.gui.grid_frame.grid_slaves(
            row=0, column=1)[0] == self.gui.master.focus_get())
        # Test moving to the first cell of the next row
        self.gui.move_to_next_cell(0, 8)
        self.assertTrue(self.gui.grid_frame.grid_slaves(
            row=1, column=0)[0] == self.gui.master.focus_get())

    def test_move_focus(self):
        """Test moving focus to the adjacent cell based on arrow key pressed"""
        event = "<Left>"
        self.gui.move_focus(event, 0, 1, 0, -1)
        self.assertTrue(self.gui.grid_frame.grid_slaves(
            row=0, column=0)[0] == self.gui.master.focus_get())

    def test_create_grid(self):
        """Test creating the grid"""
        self.assertEqual(len(self.gui.grid_frame.grid_slaves()), 81)
        self.assertIsInstance(self.gui.grid_frame.grid_slaves()[0], Entry)

    def test_create_buttons(self):
        """Test creating buttons"""
        self.assertEqual(len(self.gui.button_frame.grid_slaves()), 2)
        self.assertIsInstance(self.gui.button_frame.grid_slaves()[0], Entry)

    @patch('tkinter.Toplevel')
    @patch('tkinter.Text')
    def test_show_detailed_message(self, mock_text, mock_toplevel):
        """Test showing detailed message in a dialog"""
        message = "This is a detailed message."

        # Create a mock instance for the dialog
        mock_dialog_instance = MagicMock()
        mock_toplevel.return_value = mock_dialog_instance

        # Call the method to test
        self.gui.show_detailed_message(message)

        # Assertions
        mock_toplevel.assert_called_once()  # Check if Toplevel was called
        mock_dialog_instance.title.assert_called_once_with(
            "No Solution!")  # Check if title was set
        mock_dialog_instance.iconbitmap.assert_called_once_with(
            # Check if icon was set
            self.gui.resource_path(r"icons\sudoku-icon.ico"))
        mock_text.assert_called_once_with(
            mock_dialog_instance, wrap="word", height=10, width=40)  # Check if Text was called
        mock_text_instance = mock_text.return_value  # Get the mock Text instance
        mock_text_instance.pack.assert_called_once_with(
            fill="both", expand=True, padx=10, pady=10)  # Check if pack was called
        mock_text_instance.tag_configure.assert_called_once_with(
            "left", justify="left")  # Check if tag_configure was called
        mock_text_instance.insert.assert_called_once_with(
            "1.0", message, "left")  # Check if insert was called
        mock_text_instance.config.assert_called_once_with(
            state="disabled")  # Check if config was called
        mock_dialog_instance.resizable.assert_called_once_with(
            True, True)  # Check if resizable was called
        mock_dialog_instance.transient.assert_called_once()  # Check if transient was called
        mock_dialog_instance.grab_set.assert_called_once()  # Check if grab_set was called
        mock_dialog_instance.focus_set.assert_called_once()  # Check if focus_set was called
        mock_dialog_instance.wait_window.assert_called_once()

    def test_resource_path(self):
        """Test getting the correct resource path"""
        relative_path = r"icons\sudoku-icon.ico"
        icon_path = self.gui.resource_path(relative_path)
        self.assertTrue(os.path.exists(icon_path))

    def test_clear(self):
        """Test clearing all entries in the puzzle"""
        for i in range(9):
            for j in range(9):
                self.gui.puzzle[i][j].set("1")
        self.gui.clear()
        for i in range(9):
            for j in range(9):
                self.assertTrue(self.gui.puzzle[i][j].get() == "")

    def tearDown(self):
        """Tear down the test environment after each test case"""
        self.gui.master.destroy()


if __name__ == "__main__":
    unittest.main()
