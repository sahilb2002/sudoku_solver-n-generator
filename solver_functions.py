from cv2 import solve, sqrt
from pysat.solvers import Solver
from pysat.formula import CNF
import pysat
import numpy as np
from time import time
import random

def add_number_constrain(sudoku_cnf,n,k):
    for s in range(n):
        for r in range(k**4):
            atleast_1 = list(np.arange(r*k**2+1+s*k**6 , r*k**2+k**2+1+s*k**6))
            sudoku_cnf.append(atleast_1)
            for m1 in range(1,k**2):
                for m2 in range(m1+1,k**2+1):
                    sudoku_cnf.append([-(r*k**2+m1+s*k**6),-(r*k**2+m2+s*k**6)])

def add_row_constrain(sudoku_cnf,n,k):
    for i in range(k**2):
        for m in range(1,k**2+1):
            for s in range(n):
                row = list(np.arange(i*k**4+m+s*k**6 , i*k**4+k**4+m+s*k**6 , k**2))
                sudoku_cnf.append(row)
                for j1 in range(k**2-1):
                    for j2 in range(j1+1,k**2):
                        sudoku_cnf.append([-(s*k**6 + (i*k**2+j1)*k**2 + m) , -(s*k**6 + (i*k**2+j2)*k**2 + m)])

def add_column_constrain(sudoku_cnf,n,k):
    for r in range(k**2):
        for m in range(1,k**2+1):
            for s in range(n):
                col = list(np.arange(r*k**2+m+s*k**6 , r*k**2+k**6+m+s*k**6 , k**4))
                sudoku_cnf.append(col)
                for i1 in range(k**2-1):
                    for i2 in range(i1+1,k**2):
                        sudoku_cnf.append([-(s*k**6 + (i1*k**2 + r)*k**2 + m) , -(s*k**6 + (i2*k**2 + r)*k**2 + m)])

def add_grid_constrain(sudoku_cnf,n,k):
    for a in range(k):
        for b in range(k):
            for s in range(n):
                for m in range(1,k**2+1):
                    grid = []
                    for j in range(a*k**4+b*k**2 , a*k**4+b*k**2+k**4 , k**3):
                        grid = grid + list(np.arange(j*k+m+s*k**6 , j*k+k**3+m+s*k**6 , k**2))
                    sudoku_cnf.append(grid)
                    for g1 in range(k-1):
                        for g2 in range(g1+1,k):
                            sudoku_cnf.append([-(s*k**6 + ((a*k+int(g1/k))*k**2 + b*k + g1%k)*k**2 + m ), -(s*k**6 + ((a*k+int(g2/k))*k**2 + b*k + g2%k)*k**2 + m)])

def add_pair_constrain(sudoku_cnf,n,k):
    for r in range(k**4):
        for m in range(1,k**2+1):
            for s1 in range(n-1):
                for s2 in range(s1+1,n):
                    sudoku_cnf.append([-(r*k**2 + m + s1*k**6) , -(r*k**2 + m + s2*k**6)])

def add_basic_constrain(k,n,sudoku_basic):
    # sudoku_basic = CNF()
    add_number_constrain(sudoku_basic,n,k)
    add_row_constrain(sudoku_basic,n,k)
    add_column_constrain(sudoku_basic,n,k)
    add_grid_constrain(sudoku_basic,n,k)
    add_pair_constrain(sudoku_basic,n,k)
    # return sudoku_basic

def add_specific_constrain(n,k,sudokus,basic,specific):
    for s in range(n):
        for i in range(k**2):
            for j in range(k**2):
                r = i*k**2 + j
                m = int(sudokus[s][i,j])
                if(m==0):
                    continue
                basic.append([int(s*k**6 + r*k**2 + m)])
    if(len(specific)!=0):
        basic.append(specific)
    
def solve_sudoku(n,k,sudokus,sudoku_const,specific = [],randomized=False,verbose=False):

    # add constrains
    add_specific_constrain(n,k,sudokus,sudoku_const,specific)
    # clausses = [[int(s) for s in sublist] for sublist in sudoku_const.clauses]
    clausses = sudoku_const.clauses

    if(randomized):
        for sub in clausses:
            random.shuffle(sub)
        random.shuffle(clausses)

    if(verbose):
        print("no. of clausses = ",len(clausses))
        print("all contrain added!! Solving...")
        
    # solve using a sat solver
    start = time()
    sudoku_solver = Solver("g3",bootstrap_with=clausses)   # this statement is alone taking too much time due to adding so many clauses...
    # sudoku_solver.append_formula(clausses,no_return=False)
    sudoku_solver.solve()
    stop = time()
    model = sudoku_solver.get_model()


    if(model==None):
        if(verbose):
            print("No possible sollution :(")
            print("Time taken = ",stop-start)
        return (False,None)
    
    elif (verbose):
        print("solved :)")
        print("Time taken = ",stop-start)

    return (True,model)

def fill_sudoku(n,k,sudokus,model):
    # fill incomplete sudoku
    for a in model:
        if(a<0):
            continue
        s = int((a-1)/k**6)
        r = int((a - s*k**6-1)/k**2)
        m = a - s*k**6 - r*k**2
        row = int(r/k**2)
        col = r%k**2
        sudokus[s][row,col] = int(m)
