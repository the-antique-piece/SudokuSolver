"""
 metadata files (setup.py or pyproject.toml) that define the project's structure and dependencies.
"""
from setuptools import setup, find_packages

setup(
    name='SudokuSolver',
    version='1.0',
    packages=find_packages(),
    python_requires='>=3.11.3',  # Specify the minimum Python version required
    install_requires=[
        # List your dependencies here # 'numpy',
        # No external dependencies are needed for tkinter#'matplotlib'
    ],
)
