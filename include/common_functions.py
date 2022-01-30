from random import sample
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

def print_csv(mat,file_name):
    c=len(mat)
    m, n =mat[0].shape
    
    f=open(file_name, 'w', newline='')
    write = csv.writer(f)
    for s in range(c):
        write.writerows(mat[s])
        print('', file=f)
    
    f.close()

   

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

def valid_pair(mat):
    c=len(mat)
    m, n =mat[0].shape
    k = int(np.sqrt(m))
    for s1 in range(c-1):
        for s2 in range(s1+1, c):
            for i in range(m):
                for j in range(n):
                    if(mat[s1][i,j]==mat[s2][i,j]):
                        return False
    
    for s in range(c):
        for i in range(m):
            if(len(set(mat[s][i]))!=n):
                return False
        
        for i in range(n):
            col=[item[i] for item in mat[s]]
            if(len(set(col))!=m):
                return False
        
        for i in range(0, m, k):
            for j in range(0, n, k):
                vals=mat[s][i][j:j+k]
                for l in range (1, k):
                    vals=np.append(vals,mat[s][i+l][j:j+k])
                
                if(len(set(vals))!=m):
                    return False
        
    return True


