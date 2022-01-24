from matplotlib.style import available
import numpy as np
import random
import pysat
from solver_functions import *
from time import time
from helper_functions import *

# def randomly_fill_diag(sudoku,k,diag=0):
#     grids = np.random.permutation(k)
#     rows = np.random.permutation(k)
#     cols = np.random.permutation(k)

#     for r in grids:
#         available_nos = list(np.random.permutation(np.arange(1,k**2+1)))
#         start_col = 0
#         start_row = 0
#         if(diag==0):
#             start_row = r*k
#             start_col = r*k
#         else:
#             start_row = r*k
#             start_col = k**2 - r*k - k
#         for i in rows:
#             for j in cols:
#                 sudoku[start_row+i,start_col+j] = available_nos.pop(0)
                


def generate_fully_filled(k,n):

    sudokus = []
    for i in range(n):
        sudokus.append(np.zeros([k**2,k**2],dtype=int))

    # randomly_fill_diag(sudokus[0],k,0)
    # randomly_fill_diag(sudokus[1],k,1)

    ch,sol = solve_sudoku(n,k,sudokus,randomized=True)
    if(ch):
        # print_mat(sudokus)
        fill_sudoku(n,k,sudokus,sol)
    else:
        print("This should not get printed ever!!")
    return sudokus


def get_index(k,a,n=1):
    s = int(a/k**4)
    r = int(a - s*k**4)
    row = int(r/k**2)
    col = r%(k**2)
    return (s,row,col)

def remove_nums(n,k,sudokus):
    to_be_cheked = list(np.random.permutation(n*(k**4)))
    removed = []
    cant_remove = []
    i=1
    while len(to_be_cheked)!=0:
        print(i,"th iteration started. No. of entries removed so far = ",len(removed))
        i+=1
        a = to_be_cheked.pop(0)
        s,r,c = get_index(k,a,n)
        m = int(sudokus[s][r,c])
        removed.append(-(a*(k**2)+m))
        sudokus[s][r,c] = 0
        check,sol = solve_sudoku(n,k,sudokus,specific = removed)
        if(check):
            sudokus[s][r,c] = m
            removed.pop()
            cant_remove.append(a)
    print("no of entries removed = ",len(removed))
        
def main():
    n=2
    k=3
    start = time()
    sudokus = generate_fully_filled(k,n)
    stop = time()
    print("generated sudoku..")
    print_sudokus(sudokus)
    print("time taken to generate this = ",stop-start)
    start = time()
    remove_nums(n,k,sudokus)
    stop = time()
    print_sudokus(sudokus)
    print("time taken = ",stop-start)

main()
