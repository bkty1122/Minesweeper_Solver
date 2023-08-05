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
        a = self.counting_step(state_trans)
        # converting the state object into a np array, unknown = nan, opened cell = 0, marked mine = 1
        # marked flag would be shown in 'self.known' database
        # if not np.isnan(state_trans).all():
        #     self.known[~np.isnan(state_trans)] = 0 
            
        #     # prob, _state_trans = self._counting_step(state_trans)
        #     # if self._stop_at_solution and ~np.isnan(prob).all() and 0 in prob:
        #     #     return prob
        #     # prob = self._cp_step(_state_trans, prob)
        #     # return prob
        
        # else:
        return np.full((self._rows,self._cols), self._total_mines / (self._rows * self._cols)), a
    def counting_step(self, state):
        result = np.full((self._rows,self._cols), np.nan)
        state_ck = reduce_numbers(state, self.known == 1)
        state_ck_zero_mask = np.full((self._rows,self._cols), True)
        if state_ck.size - np.count_nonzero(np.isnan(state_ck)) > 0:
            state_ck_zero = np.argwhere(state_ck == 0) # return which [x,y] in state_check is 0
            for i in range(len(state_ck_zero)):
                a = neighbors_xy(state_ck_zero[i][1], state_ck_zero[i][0], (self._rows, self._cols))
                state_ck_zero_mask = state_ck_zero_mask & ~a #return a boolean array, state which are the neighbours of sale cells
            state_ck_zero_mask = np.isnan(self.known) & ~state_ck_zero_mask #combine with bool np.isnan and ~state_ck_zero_mask
            result = np.where(state_ck_zero_mask == True, 0, np.nan) 
            return result
        return result
    # def _cp_step(self, state):
    #     pass
    def trial(self):
        self.known[1,1] = 0
        self.known[1,3] = 1
        self.known[2,5] = 1
        self.known[5,2] = 1
        self.known[5,3] = 1
        self.known[4,2] = 0
        self.known[4,3] = 0
        playerboard[1][1] = gameboard[1][1]
        playerboard[1][4] = gameboard[1][4]
        playerboard[4][2] = gameboard[4][2]
        playerboard[4][3] = gameboard[4][3]
        print(np.array(playerboard))
        print(self.known)
        print(self.solve())

trial_minesweeper = Minesweeper_solver(7,7,7)
trial_minesweeper.trial()