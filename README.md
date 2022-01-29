# Sudoku Solver and Generator
## **CS202 Assignment-1**
-Prof. Subhajit Roy 
#### Submitted BY-
Sahil Bansal <br> 200836

Parth Maniar <br> 200671

### **Problem Statement**
In this question, you have to write a k-sudoku puzzle pair solver and generator by encoding the problem to propositional logic and solving it via a SAT solver (https://pysathq.github.io/). 

Given a sudoku puzzle pair S1, S2 (both of dimension k) as input, your job is to write a program to fill the empty cells of both sudokus such that it satisfies the following constraints, <br>
Individual sudoku properties should hold. <br>
For each empty cell S1[i, j] ≠ S2[i, j], where i is row and j is column.

**Input**: Parameter k, <br> 
single CSV file containing two sudokus. The first k* k rows are for the first sudoku and the rest are for the second sudoku. Each row has k* k cells. Each cell contains a number from 1 to k*k. Cell with 0 specifies an empty cell.
<br>
**Output**: If the sudoku puzzle pair doesn't have any solution, you should return None otherwise return the filled sudoku pair.

In the second part, you have to write a k-sudoku puzzle pair generator. The puzzle pair must be maximal (have the largest number of holes possible) and must have a unique solution. 

**Input**: Parameter k <br>
**Output**: CSV file containing two sudokus in the format mentioned in Q1.

### Generalization-
We generalize the problem statement by including not just a pair of sudokus but a n-tuple of sudokus. Each pair of these n sudokus satisfy these constrains.
### **Notations**
<ul>
<li>n : number of sudokus given (defaults to 2) .</li>
<li>k : size of sudoku as given in problem statement.</li>
<li>s : id of sudoku, in the range [0,n-1]. </li>
<li>i,j : row,column number of cell (indexing starts from 0).</li>
<li>r = i &sdot; k<sup>2</sup> + j : id of a cell of sudoku. </li>
<li>
Prepositions : <br> 
Since pysat represents a boolean variables as natural numbers, we also define our propositions in form of numbers- <br>
p(s,i,j,m) = s &sdot; k<sup>6</sup> + i &sdot; k<sup>4</sup> + j &sdot; k<sup>2</sup> + m = the entry in i<sup>th</sup> row and j<sup>th</sup> column of s<sup>th</sup> sudoku is m.
</li>
</ul>

### **Encoding**
After defining the propositions as above we can encode the problem into a propositional formula by adding following constrains-
<ol>
<li>Each cell must have at least one number- <br>
&forall; s, i, j: [&or;<sub>m</sub> p(s, i, j, m)]
</li>

<li>Each cell can have atmost one element- <br>
&forall; s, i, j, m1, m2: [&not;p(s, i, j, m1) &or; &not;p(s, i, j, m2)]
</li>

<li>
Every number must be present in each row- <br>
&forall; s, i, m: [&or;<sub>j</sub> p(s, i, j, m)]
</li>

<li>
Every number must be present in each column- <br>
&forall; s, j, m: [&or;<sub>i</sub> p(s, i, j, m)]
</li>

<li>
Every number must be present in each subgrid- <br>
&forall; s, is, js, m: [&or;<sub>i</sub> &or;<sub>j</sub> p(s, is+i, js+j, m)]
</li>

<li>
In corresponding cells of each pair of sudokus same number must not be present- <br>
&forall; s1, s2, i, j, m: [&not;p(s1, i, j, m) &or; &not;p(s2, i, j, m)]
</li>
</ol>

After creating a solver with these encodings we made following two observations-
<ol>
<li> The solver was able to solve partially filled sudokus efficiently.</li>
<li>But the efficiency decreases as the number of filled entries decreases. If all entries are 0 it takes very long time to solve.</li>
</ol>

We came to conclusion that the more constrained the solver is more efficient it is.<br>
So we added these redundant constrains-
<ol>
<li>
Every number must be present in at most one cell in every row- <br>
&forall; s, i, j1, j2, m: [&not;p(s, i, j1, m) &or; &not;p(s, i, j2, m)]
</li>

<li>
Every number must be present in at most one cell in every column- <br>
&forall; s, i1, i2, j, m: [&not;p(s, i1, j, m) &or; &not;p(s, i2, j, m)]
</li>

<li>
Every number must be present in at most one cell in every subgrid- <br>
&forall; s, is, js, i1, j1, i2, j2, m: [&not;p(s, is &sdot; k + i1, js &sdot; k + j1, m) &or; &not;p(s, is &sdot; k + i2, js &sdot; k + j2, m)]
</li>
</ol>
After adding all these constrains our solver becomes more efficient at least for empty sudokus.

### **Sudoku generation**

The major steps in genearting sudokus are-
<ol>
<li> Genrate a random fully filled tuple of sudokus satisfying all given constrains</li>
<li> Create a list of all entries in sudokus, let this list be l. Add a clause to solver so that solver looks for solutions other than this solution ( &not;l). </li>
<li>For each entry in sudoku do-
<ol type=a>
<li>
Remove it temporarily and solve the obtained sudokus.
</li>
<li>
If a solution exists add this entry back to sudoku (removing this entry would create two possible solutions). Otherwise remove this entry permanently.
</li>
</ol>
</li>
</ol>

#### Generating fully filled sudoku
to be filled...

### **Code Structure**
The include folder contains two files- <br>
<ul>
<li> solver_class.py: This file contains code for a class, sudoku_solver. This class has all the methods of adding constains to a pysat solver object. The solve() method of this class solves the given sudokus.
</li>
<li>common_functions.py: contains some functions for input/ouput and testing.
</li>
</ul>

The file **sudoku_solver.py** can be used to solve given sudoku-
```
python3 sudoku_solver.py path/to/file_containing_sudoku.csv
```

The file **sudoku_generator.py** contains code for generating sudoku and can be used as-
```
python3 sudoku_generator.py k n
```
The argument n is optional, its default value is 2. 