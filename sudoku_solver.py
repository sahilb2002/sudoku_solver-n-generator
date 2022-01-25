from helper_functions import *
import numpy as np
from time import time
from solver_class import *


sudokus,n,k = take_input("test_cases/test_case8_25by25.txt")
print("Given sudoku...")
print_sudokus(sudokus)

solve1 = sudoku_solver(n,k)
check,sol = solve1.solve(sudokus,verbose = True)

if(check):
    fill_sudoku(n,k,sudokus,sol)
    print_sudokus(sudokus)
