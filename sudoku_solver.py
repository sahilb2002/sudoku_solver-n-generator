from solver_functions import *
from helper_functions import *
import numpy as np
from time import time



sudokus,n,k = take_input("test_cases/test_case8_25by25.txt")
print("Given sudoku...")
print_sudokus(sudokus)

check,sol = solve_sudoku(n,k,sudokus,verbose=True)

if(check):
    fill_sudoku(n,k,sudokus,sol)
    print_sudokus(sudokus)

