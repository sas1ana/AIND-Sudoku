# AIND-Sudoku

# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# 
Question 1 (Naked Twins)

Q: 
How do we use constraint propagation to solve the naked twins problem?  

A: 
The constraint propagation algorithm proceeds as follows. When a given sudoku is assigned to system, the algorithm computes the possible value sets and assigned values of all its dependent variables. This process continues recursively until there are no more changes in the puzzle.More specifically, when an element X changes its value, the system evaluates the possible expression of each element Y dependent on X. This may generate a new set of possible values for other elements. If this set changes, the preference constraint is evaluated selecting one of the possible values like we did it with Backtracking as the new assigned value for Y. If this assigned value is different from the previous one, it causes the system to recompute the values for further downstream elements.

Here Naked Twin strategy adds additional constraint dimension which certainly makes the algorithm better equip to solve sudoku before diving into trial & error.
Question 2 (Diagonal Sudoku)

Q: 
How do we use constraint propagation to solve the diagonal sudoku problem?  

A: 
Diagonal Sudoku is just a special case of general sudoku. This adds additional constraints onto the diagonals. By adding diagonal constraints definition into unitlist we could achieve the same. Adding constraints to the problem gives fewer chance to go on to propagation for trial & error. This speeds up the process to solve it more quickly.



Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
