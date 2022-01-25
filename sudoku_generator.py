import numpy as np
import random
from solver_class import *
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
    fully_filled = sudoku_solver(n,k,randomized=True)
    ch,sol = fully_filled.solve(sudokus)
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

def remove_k2_nums(n,k,sudokus,to_be_checked,removed):
    remove = []
    for i in range(k**2):
        a = to_be_checked.pop(0)
        remove.append(a)
        s,row,col = get_index(k,a,n)
        removed.append(-(a*k**2 + sudokus[s][row,col]))
        sudokus[s][row][col] = 0
    return remove

def restore_mistake(n,k,sudokus,remove,removed,to_be_checked):
    for i,a in enumerate(remove):
        num = -removed.pop(-k**2+i)
        m = num%(k**2)
        assert (int((num-1)/(k**2)) == a)
        to_be_checked.insert(0,a)
        s,r,c = get_index(k,a,n)
        sudokus[s][r,c] = m

def remove_1_num(n,k,sudokus,s_solver,to_be_checked,removed,cant_remove):
    a = to_be_checked.pop(0)
    s,r,c = get_index(k,a,n)
    m = int(sudokus[s][r,c])
    removed.append(-(a*(k**2)+m))
    sudokus[s][r,c] = 0
    check,sol = s_solver.solve(sudokus)
    if(check):
        sudokus[s][r,c] = m
        removed.pop()
        cant_remove.append(a)


def remove_nums(n,k,sudokus):
    to_be_cheked = list(np.random.permutation(n*(k**4)))
    removed = []
    cant_remove = []
    i=1
    s_solver = sudoku_solver(n,k)
    s_solver.add_unique_sol_constrain(sudokus)

    while len(to_be_cheked)!=0:
        print("\rNo of entries checked = ",n*k**4-len(to_be_cheked)," out of ",n*k**4,", entries removed = ",len(removed),end="")

        if(len(to_be_cheked)>(n*k**4/2 + k**2)):
            rem = remove_k2_nums(n,k,sudokus,to_be_cheked,removed)
            ch,sol = s_solver.solve(sudokus)

            if(ch):
                print("\nextra entries removed. restoring mistake...")
                restore_mistake(n,k,sudokus,rem,removed,to_be_cheked)
                for i in range(k**2):
                    remove_1_num(n,k,sudokus,s_solver,to_be_cheked,removed,cant_remove)
        
        else:
            remove_1_num(n,k,sudokus,s_solver,to_be_cheked,removed,cant_remove)

    print("\nTotal no of entries removed = ",len(removed))
        
def main():
    n=4
    k=4
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
