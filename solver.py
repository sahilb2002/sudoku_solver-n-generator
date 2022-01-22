from cv2 import solve, sqrt
from pysat.solvers import Solver
from pysat.formula import CNF
import numpy as np
from time import time

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

def add_column_constrain(sudoku_cnf,n,k):
    for r in range(k**2):
        for m in range(1,k**2+1):
            for s in range(n):
                col = list(np.arange(r*k**2+m+s*k**6 , r*k**2+k**6+m+s*k**6 , k**4))
                sudoku_cnf.append(col)

def add_grid_constrain(sudoku_cnf,n,k):
    for a in range(k):
        for b in range(k):
            for s in range(n):
                for m in range(1,k**2+1):
                    grid = []
                    for j in range(a*k**4+b*k**2 , a*k**4+b*k**2+k**4 , k**3):
                        grid = grid + list(np.arange(j*k+m+s*k**6 , j*k+k**3+m+s*k**6 , k**2))
                    sudoku_cnf.append(grid)

def add_pair_constrain(sudoku_cnf,n,k):
    for r in range(k**4):
        for m in range(1,k**2+1):
            for s1 in range(n-1):
                for s2 in range(s1+1,n):
                    sudoku_cnf.append([-(r*k**2 + m + s1*k**6) , -(r*k**2 + m + s2*k**6)])

def add_basic_constrain(k,n):
    sudoku_basic = CNF()
    add_number_constrain(sudoku_basic,n,k)
    add_row_constrain(sudoku_basic,n,k)
    add_column_constrain(sudoku_basic,n,k)
    add_grid_constrain(sudoku_basic,n,k)
    add_pair_constrain(sudoku_basic,n,k)
    return sudoku_basic

def add_specific_constrain(n,k,sudokus,basic):
    for s in range(n):
        for i in range(k**2):
            for j in range(k**2):
                r = i*k**2 + j
                m = int(sudokus[s][i,j])
                if(m==0):
                    continue
                basic.append([int(s*k**6 + r*k**2 + m)])
    
def solve_sudoku(n,k,sudokus):

    # add constrains

    print("adding constrains")
    sudoku_const = add_basic_constrain(k,n)
    add_specific_constrain(n,k,sudokus,sudoku_const)
    clausses = [[int(s) for s in sublist] for sublist in sudoku_const.clauses]
    print("no. of clausses = ",len(clausses))
    print("all contrain added!! Solving...")
    
    # solve using a sat solver
    sudoku_solver = Solver("g3")
    sudoku_solver.append_formula(clausses,no_return=False)
    start = time()
    sudoku_solver.solve()
    stop = time()
    model = sudoku_solver.get_model()


    if(model==None):
        print("No possible sollution :(")
        print("Time taken = ",stop-start)
        return False
    else:
        print("solved :)")
        print("Time taken = ",stop-start)

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
    return True
    

def print_mat(mat):
    c = len(mat)
    m,n = mat[0].shape
    for s in range(c):
        for i in range(m):
            for j in range(n):
                print(mat[s][i,j],end=" ")
            print()
        print()

def take_input(file_name):
    data = np.loadtxt(file_name,dtype=int,delimiter=",")
    a,b = data.shape
    k = int(np.sqrt(b))
    n = int(a/(k**2))
    sudokus = []
    for i in range(n):
        sudokus.append(data[i*k**2:(i+1)*k**2,:])
    print("no of sudokus given = ",len(sudokus))
    return (sudokus,n,k)

def main():
    file = "try4.txt"
    sudokus,n,k = take_input(file)
    print("before solving")
    print_mat(sudokus)
    sol = solve_sudoku(n,k,sudokus)
    if(sol):
        print("After solving")
        print_mat(sudokus)

main()                