from helper_functions import *
import numpy as np
from time import time
from solver_class import *


sudokus,n,k = take_input("test_cases/wrong_testcase.txt")
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