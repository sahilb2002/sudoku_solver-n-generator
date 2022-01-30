import numpy as np
import random
from include.solver_class import *
from time import time
from include.common_functions import *
from sys import argv
                

def generate_fully_filled(k,n):

    sudokus = []
    for i in range(n):
        sudokus.append(np.zeros([k**2,k**2],dtype=int))
    
    # Create a valid sudoku 
    per = list(np.random.permutation(np.arange(1,k**2+1)))
    tmp = list(np.copy(per))
    for i in range(k):
        tmp = per[i:] + per[:i]
        sudokus[0][i*k,:] = np.copy(tmp)
        for j in range(1,k):
            tmp = tmp[k:] + tmp[:k]
            sudokus[0][i*k+j,:] = np.copy(tmp)

    # Shuffle its columns in set of k.
    all_cols = []
    for j in range(k):
        all_cols.append(np.copy(sudokus[0][:,j*k:j*k+k]))
    random.shuffle(all_cols)
    for i in range(k):
        all_cols[i] = all_cols[i][:,np.random.permutation(all_cols[i].shape[1])]
    sudokus[0][:,:] = np.copy(np.hstack(all_cols))

    # shuffle its rows in set of k.
    all_rows = []
    for i in range(k):
        all_rows.append(sudokus[0][i*k:i*k+k,:])
    random.shuffle(all_rows)
    for i in range(k):
        all_rows[i] = all_rows[i][np.random.permutation(all_rows[i].shape[0]),:]
    sudokus[0][:,:] = np.copy(np.vstack(all_rows))

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
        
def main(argv):
    n = 2
    k = int(argv[1])
    if len(argv)==3:
        n = int(argv[2])

    start = time()
    sudokus = generate_fully_filled(k,n)
    stop = time()
    print("generated fully filled sudoku..")
    print_sudokus(sudokus)
    print("time taken to generate this = ",stop-start)
    if(valid_pair(sudokus)):
        print("Generated pair is valid")
    start1 = time()
    remove_nums(n,k,sudokus)
    stop1 = time()
    print_sudokus(sudokus)
    print("time taken to remove entries = ",stop1-start1)
    print("Total time = ",stop1-start)
    file = input("Enter file name to save sudokus to (press enter if you dont want to save) > ")
    if(len(file)!=0):
        print_csv(sudokus,file)

assert(len(argv)==2 or len(argv)==3), "Usage: python sudoku_generator.py k n \n n is optional default is 2."
main(argv)
