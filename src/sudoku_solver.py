"""
sudoku_solver module for handling sudoku puzzle solving logic.
"""


class SudokuSolverLogic:
    """
    Class containing Sudoku puzzle solving logic.
    """

    @staticmethod
    def find_empty_cell(grid):
        """
        it searches for empty location
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    @staticmethod
    def is_valid_move(grid, row, col, num):
        """
        Checks for valid move
        """
        # Check if the number is already present in the row
        if num in grid[row]:
            return False

        # Check if the number is already present in the column
        if num in [grid[i][col] for i in range(9)]:
            return False

        # Check if the number is already present in the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False

        return True

    @staticmethod
    def solve_sudoku(grid):
        """
        This the main function that solve puzzle
        """
        # Find an empty cell in the Sudoku grid
        empty_cell = SudokuSolverLogic.find_empty_cell(grid)
        if empty_cell is None:
            return grid  # Puzzle solved, return the solved Sudoku grid

        row, col = empty_cell

        # Try placing numbers 1 to 9 in the empty cell
        for num in range(1, 10):
            if SudokuSolverLogic.is_valid_move(grid, row, col, num):
                grid[row][col] = num
                # Recursively solve the rest of the puzzle
                if SudokuSolverLogic.solve_sudoku(grid):
                    return grid  # Return the solved Sudoku grid
                # If no solution is found, backtrack
                grid[row][col] = 0

        return None  # No solution found
