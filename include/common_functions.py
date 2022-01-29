import numpy as np
import pandas as pd
import csv

def print_sudokus(mat):
    c = len(mat)
    m,n = mat[0].shape
    for s in range(c):
        for i in range(m):
            if i!=0 and i*i%m==0:
                for j in range((3*m)+4):
                    print(end="-")
                print()
            for j in range(n):
                if j!=0 and j*j%n==0:
                    print(end="|")
                if(mat[s][i,j]==0):
                    print(" .",end=" ")
                elif(mat[s][i,j]<10):
                   print("",mat[s][i,j],end=" ")
                else:
                    print(mat[s][i,j],end=" ")
            print()
            
        print('\n')

def print_csv(mat):
    c=len(mat)
    m, n =mat[0].shape
    f=open('output.csv', 'w')
    for s in range(c):
        for i in range(m):
            if i!=0 and i*i%m==0:
                for j in range((3*m)+4):
                    print(end="-", file=f)
                print('', file=f)
            for j in range(n):
                if j!=0 and j*j%n==0:
                    print(end="|", file=f)
                if(mat[s][i,j]<10):
                   print("",mat[s][i,j],end=" ", file=f)
                else:
                    print(mat[s][i,j],end=" ", file=f)
            print('', file=f)
            
        print('\n', file=f)
    f.close()

def take_input(file_name):
    data = np.loadtxt(file_name,dtype=int)
    a,b = data.shape
    k = int(np.sqrt(b))
    n = int(a/(k**2))
    sudokus = []
    for i in range(n):
        sudokus.append(data[i*k**2:(i+1)*k**2,:])
    print("no of sudokus given = ",len(sudokus))
    return (sudokus,n,k)

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