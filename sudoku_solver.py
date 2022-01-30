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
    print_csv(sudokus)

f=open('output.csv', 'a',newline='')
if(not check):
    print_csv(sudokus)
if(valid_pair(sudokus)):
    print("Sudoku Pair is a valid pair")
    print("Sudoku Pair is a valid pair", file=f)
else:
    print("Sudoku Pair is not a valid pair")
    print("Sudoku Pair is not a valid pair", file=f)