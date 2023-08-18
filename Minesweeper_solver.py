# Reference code: https://github.com/JohnnyDeuss/minesweeper-solver/blob/master/minesweeper_solver/solver.py 
# Python interpreter: 3.9.13
import numpy as np
from tools import *
from scipy.ndimage import label
from constraint import Problem, ExactSumConstraint
from functools import reduce

gameboard = [[1, 1, 1, 1, 1, 0, 0], 
             ['X', 1, 1, 'X', 2, 1, 1], 
             [1, 1, 1, 1, 2, 'X', 1],  #1, 
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
        state = np.array([[state[y][x] if isinstance(state[y][x], int) 
                           else np.nan for x in range(self._rows)] for y in range(self._cols)])
        #the state[y][x] must be written in [y][x], not [x][y], otherwise this would cause error when combining it with self.known
        if not np.isnan(state).all():
            #transfer opened cells in state_trans, marked as 0 and append knowledge in self.known
            self.known[~np.isnan(state)] = 0 
            count_result, state = self._counting_step(state)
            if 0 in count_result and self._stop_at_solution:
                self.known[count_result == 1] = 1
                return count_result
            return self.contraint_area(state) # subject to modify to test result
        return np.full((self._rows,self._cols), self._total_mines / (self._rows * self._cols))
    def _counting_step(self, state):
        """ Find all trivially easy solutions. There are 2 cases we consider:
            - A square with a 0 in it and has unflagged and unopened neighbors means that we can open all neighbors.
            - 1 square with a number that matches the number of unflagged and unopened neighbors means that we can flag
              all those neigbors.
            :param state: The unreduced state of the minefield
            :returns result: An array with known mines marked with 1, squares safe to open with 0 and everything else
                             as np.nan.
            :returns reduced_state: The reduced state, where numbers indicate the number of neighboring mines that have
                                    *not* been found.
        """
        result = np.full(state.shape, np.nan)
        # This step can be done multiple times, as each time we have results, the numbers can be further reduced.
        new_results = True
        # Subtract all numbers by the amount of neighboring mines we've already found, simplifying the game.
        state = reduce_numbers(state, self.known == 1)
        # Calculate the unknown square, i.e. that are unopened and we've not previously found their value.
        unknown_squares = np.isnan(state) & np.isnan(self.known)
        while new_results:
            num_unknown_neighbors = count_neighbors(unknown_squares)
            ### First part: squares with the number N in it and N unflagged/unopened neighbors => all mines.
            # Calculate squares with the same amount of unflagged neighbors as neighboring mines (except if N==0).
            solutions = (state == num_unknown_neighbors) & (num_unknown_neighbors > 0)
            # Create a mask for all those squares that we now know are mines. The reduce makes a neighbor mask for each
            # solution and or's them together, making one big neighbors mask.
            known_mines = unknown_squares & reduce(np.logical_or,
                [neighbors_xy(x, y, state.shape) for y, x in zip(*solutions.nonzero())], np.zeros(state.shape, dtype=bool))
            # Update our known matrix with these new finding: 1 for mines.
            self.known[known_mines] = 1
            # Further reduce the numbers, since we found new mines.
            state = reduce_numbers(state, known_mines)
            # Update what is unknown by removing known flags from the `unknown_squares` mask.
            unknown_squares = unknown_squares & ~known_mines
            # The unknown neighbor count might've changed too, so recompute it.
            num_unknown_neighbors = count_neighbors(unknown_squares)
            ### Second part: squares with a 0 in and any unflagged/unopened neighbors => all safe.
            # Calculate the squares that have a 0 in them, but still have unknown neighbors.
            solutions = (state == 0) & (num_unknown_neighbors > 0)
            # Select only those squares that are unknown and we've found to be neighboring any of the found solutions.
            # The reduce makes a neighbor mask for each solution and or's them together, making one big neighbor mask.
            known_safe = unknown_squares & reduce(np.logical_or,
                [neighbors_xy(x, y, state.shape) for y, x in zip(*solutions.nonzero())], np.zeros(state.shape, dtype=bool))
            # Update our known matrix with these new finding: 0 for safe squares.
            self.known[known_safe] = 0
            # Update what is unknown.
            unknown_squares = unknown_squares & ~known_safe
            # Now update the result matrix for both steps, 0 for safe squares, 1 for mines.
            result[known_safe] = 0
            result[known_mines] = 1
            new_results = (known_safe | known_mines).any()
        return result, state
    
    def contraint_area(self, state):
        components, num_components = self.components(state)
        result_list = []
        result = np.full(state.shape, np.nan)
        for c in range(1, num_components+1):
            result_list.append(self.guess_mine_component(state, components, c))
        # Merge the results into one single array.
        for r in result_list:
            _result = ~np.isnan(r)
            result[_result] = r[_result]
        Mine_expected = result[~np.isnan(result)].sum()
        # update known, in result returns 0 or 1
        # but first calculate expected value of mines
        Mine_expected = result[~np.isnan(result)].sum()
        result[~np.isnan(self.known)] = self.known[~np.isnan(self.known)] + 2 # 2 for safe, 3 for mine
        # update known
        self.known[result == 1] = 1
        self.known[result == 0] = 0
        # Calculate remaining Nan's weights of mine
        squares_left = np.isnan(result).sum()
        result[np.isnan(result)] = (self.mines_left() - Mine_expected) / (self._rows * self._cols - squares_left)
        return result

    def guess_mine_component(self, state, components, num_component = 1):
        '''
        return a bool array, stating which cells are neighbours of component 1
        grap each cm's neighbour (except known cells), convert to a list with their coordinates, and append to a list
        for cm with neigbours, use exactsumconstraint, variable = cm's neighbours in tuple list and [0,1], constraint = number in state
        combine solutions, use maxconstraint to filter overlapped solutions which sum is more than other cm's number
        after combining solutions, return the results
        '''
        # return a bool array, stating which cells are in component 1
        cm = neighbors(components == num_component) & ~np.isnan(state) 
        coord_cm = np.where(cm == True)
        coordinate_cm = [(x,y) for x, y in zip(coord_cm[0], coord_cm[1])] # convert to a list of tuples]
        # delete coordinate_cm[i] if it's neighbours are all known, else append to total_neigh_coord
        total_neigh_coord = []
        for i in range(len(coordinate_cm)):
            if (neighbors_xy(coordinate_cm[i][1], coordinate_cm[i][0], (self._rows, self._cols)) | np.isnan(self.known)).all():
                del coordinate_cm[i]
            else:
                cm_neigh = neighbors_xy(coordinate_cm[i][1], coordinate_cm[i][0], (self._rows, self._cols)) & np.isnan(self.known)
                cm_neighbour = np.where(cm_neigh == True) 
                coord_neigh_cm = [(x,y) for y, x in zip(cm_neighbour[1], cm_neighbour[0])] # be careful about the order of x and y
                total_neigh_coord.append(coord_neigh_cm)
        # produce a cm_index mask
        label_cm = cm.copy().astype(int) # copy cm, convert bool array to int array, otherwise we cannot assign number to cm mask
        for i in range(len(coordinate_cm)):
            (x, y) = coordinate_cm[i] #iterate tuple from coordinate_cm to map labes to label_cm
            label_cm[x,y] = i + 1
        # use label_cm and state to produce constraint, use total_neigh_coord to produce variable, append results to solutions
        solutions = []
        for j in range(len(total_neigh_coord)):
            problem = Problem()
            constraint = ExactSumConstraint(int(state[label_cm == j + 1]))
            variable = total_neigh_coord[j]
            problem.addVariables(variable, [0,1])
            problem.addConstraint(constraint)
            sol = problem.getSolutions()
            for k1 in range(len(sol)):
                # convert sol to a matrix, append to solutions
                solutions_k1 = []
                M = np.full((self._rows,self._cols), np.nan)
                M[tuple(zip(*sol[k1].keys()))] = list(sol[k1].values())
                solutions_k1.append(M)
                solutions.append([j + 1, solutions_k1])
        # now, solutions is a list of list. solutions[i][0] is the index of cm, solutions[i][1:] is the solution matrix
        # use maxconstraint to filter overlapped solutions which sum is more than other cm's number
        # use a while-loop to compare solution[i] and solution[i+1]
        i = 0
        while i < (len(solutions)-1):
            cm_index_check = 1
            while cm_index_check < (len(label_cm) + 1):
                j_list = []
                for j in range(len(solutions)):
                    if solutions[j][0] == cm_index_check:
                        j_list.append(j)
                for j in j_list:
                    if j < len(solutions):
                        bool_true = ~np.isnan(solutions[i][1:]) & ~np.isnan(solutions[j][1:])
                        if np.where(bool_true == True):
                            constraint_i_j = min(int(state[label_cm == solutions[i][0]]), int(state[label_cm == solutions[j][0]]))
                            i_array = solutions[i][1:]
                            j_array = solutions[j][1:]
                            if np.sum(np.array(i_array)[bool_true]) > constraint_i_j:
                                 del solutions[i]
                            elif np.sum(np.array(j_array)[bool_true]) > constraint_i_j:
                                del solutions[j]
                j_list.clear()
                cm_index_check += 1
            i += 1
        # now, solutions is filtered, it has removed results in which sums of overlapped cells greater than the constraint
        # build a mask for each label_cm, calculate prob for mines in each cells
        prob_semi = []
        cm_index_check = 1
        while cm_index_check < np.count_nonzero(label_cm) + 1:
            j_list = []
            for j in range(len(solutions)):
                if solutions[j][0] == cm_index_check:
                    j_list.append(j)
            j_array = [solutions[j][1:] for j in j_list]
            j_array = np.sum(np.nan_to_num(j_array, copy = False), axis = 0)
            j_array = j_array/len(j_list)
            j_array = [i for s in j_array for i in s]
            prob_semi.append(j_array)
            cm_index_check += 1
        # now, prob is a list of arrays. each array is a probability matrix for each cm
        # prob[0] is the probability matrix for cm 1, prob[1] is the probability matrix for cm 2, etc.
        # compare different non-zero element, choose the one with the highest probability;
        solutions = [solutions[i][1:] for i in range(len(solutions))]
        prob_semi_sum = np.sum(np.nan_to_num(solutions, copy= False), axis=0) / len(solutions)
        prob_semi_sum = prob_semi_sum.flatten()
        prob_semi_sum[prob_semi_sum == 0] = np.nan
        if prob_semi_sum.size == self._rows * self._cols:
            prob_semi_sum = prob_semi_sum.reshape((self._rows,self._cols))
        # must store prob_semi_sum before changing prob_semi 0 to nan
        for i in range(len(prob_semi)):
            prob_semi[i][0] = prob_semi[i][0].flatten()
            prob_semi[i][0][prob_semi[i][0] == 0] = np.nan
            if prob_semi[i][0].size == self._rows * self._cols:
                prob_semi[i][0] = prob_semi[i][0].reshape((self._rows, self._cols))
        # convert prob_semi 0 to nan 
        result = np.full((self._rows,self._cols), np.nan)
        k = 1
        while k < len(prob_semi):
            l = k - 1
            prob_semi, result = overlap_compare_replace(state, label_cm, l, k, prob_semi, result)
            if k == len(prob_semi) - 1:
                prob_semi, result = overlap_compare_replace(state, label_cm, 0, k, prob_semi, result)
            k += 1
        cm_num_mask = [components == num_component] # return a list of bool array, stating which cells are in component 1
        if np.isnan(result).all() and prob_semi_sum.shape == (self._rows, self._cols):
            return prob_semi_sum
        else:
            result_cm_num_mask = np.isnan(result) & cm_num_mask
            result_cm_num_mask = result_cm_num_mask.flatten()
            # 同樣的技術問題...
            if result_cm_num_mask.size == self._rows * self._cols:
                result_cm_num_mask = result_cm_num_mask.reshape((self._rows,self._cols))
            result[result_cm_num_mask] = 0
            return result
    
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

