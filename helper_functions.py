import numpy as np

def print_sudokus(mat):
    c = len(mat)
    m,n = mat[0].shape
    for s in range(c):
        for i in range(m):
            for j in range(n):
                print(mat[s][i,j],end=" ")
            print()
        print()

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