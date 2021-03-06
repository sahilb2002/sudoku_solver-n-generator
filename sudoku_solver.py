from asyncio import exceptions
from include.common_functions import *
import numpy as np
from time import time
from include.solver_class import *
from sys import argv

assert(len(argv)==2), "Usage: python sudoku_solver.py path/to/file_containing_sudoku.csv"
sudokus,n,k = take_input(argv[1])
print("Given sudoku...")
print_sudokus(sudokus)

solve1 = sudoku_solver(n,k)
check,sol = solve1.solve(sudokus,verbose = True)

if(check):
    fill_sudoku(n,k,sudokus,sol)
    print_sudokus(sudokus)
    if(valid_pair(sudokus)):
        print("Solver passed this test")
    else:
        print("Solver failed in this test")
