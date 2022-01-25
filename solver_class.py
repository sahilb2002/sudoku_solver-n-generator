from cgi import test
from cv2 import solve, sqrt
from pysat.solvers import Solver
from pysat.formula import CNF
import pysat
import numpy as np
from time import time
import random

class sudoku_solver:

    def __init__(self,n,k,randomized = False):
        self.n = n
        self.k = k
        self.sudoku_const = CNF()
        self.add_basic_constrain()
        clausses = [[int(s) for s in sublist] for sublist in self.sudoku_const.clauses]

        if(randomized):
            for sub in clausses:
                random.shuffle(sub)
            random.shuffle(clausses)
        self.solver = Solver('g3',bootstrap_with = clausses)

    def add_number_constrain(self):
        n = self.n
        k = self.k
        for s in range(n):
            for r in range(k**4):
                atleast_1 = list(np.arange(r*k**2+1+s*k**6 , r*k**2+k**2+1+s*k**6))
                self.sudoku_const.append(atleast_1)
                for m1 in range(1,k**2):
                    for m2 in range(m1+1,k**2+1):
                        self.sudoku_const.append([-(r*k**2+m1+s*k**6),-(r*k**2+m2+s*k**6)])

    def add_row_constrain(self):
        k = self.k
        n = self.n

        for i in range(k**2):
            for m in range(1,k**2+1):
                for s in range(n):
                    row = list(np.arange(i*k**4+m+s*k**6 , i*k**4+k**4+m+s*k**6 , k**2))
                    self.sudoku_const.append(row)
                    for j1 in range(k**2-1):
                        for j2 in range(j1+1,k**2):
                            self.sudoku_const.append([-(s*k**6 + (i*k**2+j1)*k**2 + m) , -(s*k**6 + (i*k**2+j2)*k**2 + m)])

    def add_column_constrain(self):
        k = self.k
        n = self.n

        for r in range(k**2):
            for m in range(1,k**2+1):
                for s in range(n):
                    col = list(np.arange(r*k**2+m+s*k**6 , r*k**2+k**6+m+s*k**6 , k**4))
                    self.sudoku_const.append(col)
                    for i1 in range(k**2-1):
                        for i2 in range(i1+1,k**2):
                            self.sudoku_const.append([-(s*k**6 + (i1*k**2 + r)*k**2 + m) , -(s*k**6 + (i2*k**2 + r)*k**2 + m)])

    def add_grid_constrain(self):
        k = self.k
        n = self.n

        for a in range(k):
            for b in range(k):
                for s in range(n):
                    for m in range(1,k**2+1):
                        grid = []
                        for j in range(a*k**4+b*k**2 , a*k**4+b*k**2+k**4 , k**3):
                            grid = grid + list(np.arange(j*k+m+s*k**6 , j*k+k**3+m+s*k**6 , k**2))
                        self.sudoku_const.append(grid)
                        for g1 in range(k-1):
                            for g2 in range(g1+1,k):
                                self.sudoku_const.append([-(s*k**6 + ((a*k+int(g1/k))*k**2 + b*k + g1%k)*k**2 + m ), -(s*k**6 + ((a*k+int(g2/k))*k**2 + b*k + g2%k)*k**2 + m)])

    def add_pair_constrain(self):
        k = self.k
        n = self.n
        for r in range(k**4):
            for m in range(1,k**2+1):
                for s1 in range(n-1):
                    for s2 in range(s1+1,n):
                        (self.sudoku_const).append([-(r*k**2 + m + s1*k**6) , -(r*k**2 + m + s2*k**6)])

    def add_basic_constrain(self):
        # sudoku_basic = CNF()
        self.add_number_constrain()
        self.add_row_constrain()
        self.add_column_constrain()
        self.add_grid_constrain()
        self.add_pair_constrain()
        # return sudoku_basic

    def get_specific_constrain(self,sudokus,a=1):
        k = self.k
        n = self.n
        specific = []
        for s in range(n):
            for i in range(k**2):
                for j in range(k**2):
                    r = i*k**2 + j
                    m = int(sudokus[s][i,j])
                    if(m==0):
                        continue
                    specific.append(a*int(s*k**6 + r*k**2 + m))
        return specific
    
    def add_unique_sol_constrain(self,sudokus):
        k = self.k
        n = self.n
        uniquness = self.get_specific_constrain(sudokus,a=-1)
        self.solver.add_clause(uniquness)
    
    def solve(self,sudokus,verbose=False):

        specific = self.get_specific_constrain(sudokus)

        start = time()
        self.solver.solve(assumptions=specific)
        stop = time()

        model = self.solver.get_model()

        if(model==None):
            if(verbose):
                print("No possible sollution :(")
                print("Time taken = ",stop-start)
            return (False,None)

        elif (verbose):
            print("solved :)")
            print("Time taken = ",stop-start)

        return (True,model)
