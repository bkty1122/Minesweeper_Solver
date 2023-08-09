import numpy as np
import constraint as cp
from tools import *

board = [[1, 0, 0, 0, 0, 0, 0], 
             [0, 1, 1, 0, 2, 0, 0], 
             [0, 1, 1, 1, 0, 0, 1], 
             [0, 0, 0, 0, 2, 2, 1], 
             [0, 1, 0, 3, 0, 1, 0], 
             [0, 1, 0, 0, 3, 2, 1], 
             [0, 1, 2, 2, 0, 0, 1]]

board_trial = np.array(board)
board_trans = np.array([[board_trial[y][x] if board_trial[y][x] != 0
                    else np.nan for x in range(7)] for y in range(7)])
constraint = np.full((7,7), None, dtype=object)
for i in range(7):
    for j in range(7):
        if ~np.isnan(board_trans[i,j]):
            y = cp.ExactSumConstraint(int(board_trans[i,j]))
            constraint[i,j] = y
problem = cp.Problem()
for i in range(7):
    for j in range(7):
        if constraint[i,j] != None:
            problem.addVariable(neighbors_xy(i,j,(7,7)), [0,1])
            problem.addConstraint(constraint[i,j])
            print(problem.getSolution())