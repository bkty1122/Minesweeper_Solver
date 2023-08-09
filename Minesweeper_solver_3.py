# Reference code: https://github.com/JohnnyDeuss/minesweeper-solver/blob/master/minesweeper_solver/solver.py 
import numpy as np
import random as rand
from tools import *
from scipy.ndimage import label
from constraint import Problem, ExactSumConstraint, MaxSumConstraint
from operator import mul
from functools import reduce



gameboard = [[1, 1, 1, 1, 1, 0, 0], 
             ['X', 1, 1, 'X', 2, 1, 1], 
             [1, 1, 1, 1, 2, 'X', 1], 
             [0, 0, 0, 1, 2, 2, 1], 
             [0, 1, 2, 3, 'X', 1, 0], 
             [0, 1, 'X', 'X', 3, 2, 1], 
             [0, 1, 2, 2, 2, 'X', 1]]
playerboard = [['-' for x in range(7)] for y in range(7)]

class Minesweeper_solver():
    def __init__(self, rows, cols, total_mines, stop_at_solution = True):
        self._rows = rows
        self._cols = cols
        self.known = np.full((rows, cols), np.nan)
        self._total_mines = total_mines
        self._stop_at_solution = stop_at_solution
    def known_mines_count(self):
        return np.count_nonzero(self.known == 1) # it really works!
    def known_safe_count(self):
        return np.count_nonzero(self.known == 0) # it really works also!
    def mines_left(self):
        return self._total_mines - self.known_mines_count()
    def solve(self, state = playerboard.copy()):
        state_trans = np.array([[state[y][x] if isinstance(state[y][x], int) 
                           else np.nan for x in range(self._rows)] for y in range(self._cols)])
        #the state[y][x] must be written in [y][x], not [x][y], otherwise this would cause error when combining it with self.known
        if not np.isnan(state_trans).all():
            #transfer opened cells in state_trans, marked as 0 and append knowledge in self.known
            self.known[~np.isnan(state_trans)] = 0 
            count_result = self.counting_step(state_trans)
            if 0 in count_result and self._stop_at_solution:
                return count_result
            return self.contraint_area(state_trans) # subject to modify to test result
        return np.full((self._rows,self._cols), self._total_mines / (self._rows * self._cols))
    def counting_step(self, state):
        #only return results that must be safe to open, stating as 0 in the result. 
        result = np.full((self._rows,self._cols), np.nan)
        state_ck = reduce_numbers(state, self.known == 1)
        state_ck_zero_mask = np.full((self._rows,self._cols), True)
        if state_ck.size - np.count_nonzero(np.isnan(state_ck)) > 0: # if there's 0 in state_ck
            state_ck_zero = np.argwhere(state_ck == 0) # return which [x,y] in state_check is 0
            for i in range(len(state_ck_zero)):
                a = neighbors_xy(state_ck_zero[i][1], state_ck_zero[i][0], (self._rows, self._cols))
                state_ck_zero_mask = state_ck_zero_mask & ~a #return a boolean array, state which are the neighbours of sale cells
            state_ck_zero_mask = np.isnan(self.known) & ~state_ck_zero_mask #combine with bool np.isnan and ~state_ck_zero_mask
            result = np.where(state_ck_zero_mask == True, 0, np.nan) 
            return result
        return result
        
    def contraint_area(self, state):
        components, num_components = self.components(state)
        constraint = np.full((self._rows,self._cols), None, dtype=object)
        for i in range(1, num_components + 1):
            cm = neighbors(components == i) & ~np.isnan(state)
            y =[ExactSumConstraint(int(num)) for num in state[cm]]
            constraint[cm] = y
        # for now, the constraint array contains the exactsumconstraint, stated from the number in the state
        # now: how can we make the problem knows the constraint? 
        return self.guess_mine_component(state, components)
    
    def guess_mine_component(self, state, components, num_component = 1):
        c = (components == num_component) & np.isnan(self.known) 
        # return a bool array, stating which cells are in component 1
        cm = neighbors(components == num_component) & ~np.isnan(state) 
        # return a bool array, stating which cells are neighbours of component 1
        # grap each cm's neighbour (except known cells), convert to a list with their coordinates, and append to a list
        # for cm with neigbours, use exactsumconstraint, variable = cm's neighbours in tuple list and [0,1], constraint = number in state
        # combine solutions, use maxconstraint to filter overlapped solutions which sum is more than other cm's number
        # after combining solutions, return the results
        coord_cm = np.where(cm == True)
        coordinate_cm = [(x,y) for x, y in zip(coord_cm[0], coord_cm[1])] # convert to a list of tuples
        # delete coordinate_cm[i] if it's neighbours are all known
        n = []
        for i in range(len(coordinate_cm)):
            if (neighbors_xy(coordinate_cm[i][0], coordinate_cm[i][1], (self._rows, self._cols)) | np.isnan(self.known)).all():
                del coordinate_cm[i]
            else:
                cm_neigh = neighbors_xy(coordinate_cm[i][0], coordinate_cm[i][1], (self._rows, self._cols)) & np.isnan(self.known)
                cm_neighbour = np.where(cm_neigh == True) 
                coord_neigh_cm = [(x,y) for x, y in zip(cm_neighbour[0], cm_neighbour[1])]
                n.append(coord_neigh_cm)
        # use emunurate to label list n, then generate possible mines combination using constraint module
        return n
    
    def components(self, state):
        # Get the numbers next to unknown borders.
        state_mask = ~np.isnan(state)
        label_comp, num_comp = label(state_mask) # for label encounting in state
        num_boundary_mask = [neighbors(label_comp == c) & np.isnan(state) & np.isnan(self.known) for c in range(1, num_comp +1)]
        # neighbour(label_comp == c) returns a bool array which states neighbours of label_comp, in which the array elements equal to c
        # combine the neighbour bool arrays with np.isnan(state) and np.isnan(self.known), if there's known in state and known
        # the bool would turn False
        i = 0
        while i < len(num_boundary_mask) - 1:
            j = i + 1
            while j < len(num_boundary_mask):
                if (num_boundary_mask[i] & num_boundary_mask[j]).any():
                    num_boundary_mask[i] = num_boundary_mask[i] | num_boundary_mask[j]
                    # difference between | and &: | prefer 1, & prefer 0, for this case if we use &
                    # identified neighbour cells would be eliminate, hence we need to use | instead
                    del num_boundary_mask[j]
                    i -= 1
                    break
                j += 1
            i += 1
        # for combining overlapped squares, just use the original code.
        # After generating the 1st result and combining overlapped results, re-run the similar progress
        labeled = np.zeros(state.shape)
        num_components = len(num_boundary_mask)
        for c, mask in enumerate(num_boundary_mask, 1):
            labeled[mask] = c
        # Now connect components that have a number in between them that connect them with a constraint.
        i = 1
        while i <= num_components-1:
            j = i + 1
            while j <= num_components:
                # If there is a number connecting the two components...
                if not np.isnan(state[dilate(labeled == i) & dilate(labeled == j)]).all():
                    # Merge the components.
                    labeled[labeled == j] = i
                    labeled[labeled > j] -= 1
                    num_components -= 1
                    i -= 1
                    break
                j += 1
            i += 1
        return labeled, num_components
        
    def trial(self):
        self.known[5,2] = 1
        playerboard[0][0] = gameboard[0][0]
        playerboard[0][1] = gameboard[0][1]
        playerboard[1][1] = gameboard[1][1]
        playerboard[1][4] = gameboard[1][4]
        playerboard[4][2] = gameboard[4][2]
        playerboard[4][3] = gameboard[4][3]
        playerboard[6][2] = gameboard[6][2]
        print(np.array(playerboard))
        print(self.solve())
        #print(self.known)

trial_minesweeper = Minesweeper_solver(7,7,7)
trial_minesweeper.trial()