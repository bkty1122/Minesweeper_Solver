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

# Chatgpt 4 optimize results, there's bug...
    
        #     component_mask = (components == num_component) & np.isnan(self.known)
        # component_neighbours = neighbors(component_mask) & ~np.isnan(state)

        # neighbour_coords = np.transpose(np.where(component_neighbours))
        # cell_coords = [tuple(coord) for coord in neighbour_coords]

        # total_neigh_coords = []
        # for coord in cell_coords:
        #     neighbours_mask = neighbors_xy(*coord, (self._rows, self._cols)) & np.isnan(self.known)
        #     if not neighbours_mask.all():
        #         total_neigh_coords.append([tuple(n_coord) for n_coord in np.transpose(np.where(neighbours_mask))])

        # label_cm = component_neighbours.astype(int)
        # for i, coord in enumerate(cell_coords):
        #     label_cm[coord] = i + 1

        # solutions = []
        # for i, neigh_coords in enumerate(total_neigh_coords):
        #     problem = Problem()
        #     constraint = ExactSumConstraint(int(state[label_cm == i + 1]))
        #     problem.addVariables(neigh_coords, [0, 1])
        #     problem.addConstraint(constraint)

        #     for sol in problem.getSolutions():
        #         sol_matrix = np.full((self._rows, self._cols), None, dtype=object)
        #         sol_matrix[list(zip(*sol.keys()))] = list(sol.values())
        #         solutions.append([i, sol_matrix])