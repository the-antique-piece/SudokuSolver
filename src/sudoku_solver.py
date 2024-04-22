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
    def check_duplicates(grid):
        """
        Check for duplicate values in rows, columns, and 3x3 grids.
        """
        for i in range(9):
            row_values = set()
            col_values = set()
            grid_values = set()
            for j in range(9):
                row_value = grid[i][j]
                col_value = grid[j][i]
                grid_row = 3 * (i // 3) + j // 3
                grid_col = 3 * (i % 3) + j % 3
                grid_value = grid[grid_row][grid_col]

                if row_value != 0 and row_value in row_values:
                    return False
                if col_value != 0 and col_value in col_values:
                    return False
                if grid_value != 0 and grid_value in grid_values:
                    return False

                row_values.add(row_value)
                col_values.add(col_value)
                grid_values.add(grid_value)

        return True

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
        This is the main function that solves the puzzle
        """
        # Check if the grid contains valid values (integers from 1 to 9)
        for row in grid:
            for cell in row:
                if not isinstance(cell, int) or not 0 <= cell <= 9:
                    raise ValueError(
                        "Invalid input: Sudoku grid should contain integers from 1 to 9")
        if SudokuSolverLogic.check_duplicates(grid) is False:
            return None
        else:
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
                    if SudokuSolverLogic.solve_sudoku(grid) is not None:
                        return grid  # Return the solved Sudoku grid
                    # If no solution is found, backtrack
                    grid[row][col] = 0
