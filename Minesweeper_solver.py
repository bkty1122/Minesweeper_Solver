# Reference code: https://github.com/JohnnyDeuss/minesweeper-solver/blob/master/minesweeper_solver/solver.py 
# Python interpreter: 3.9.13
import numpy as np
from tools import *
from scipy.ndimage import label
from constraint import Problem, ExactSumConstraint, MaxSumConstraint
from functools import reduce
np.set_printoptions(precision=3)

class Minesweeper_solver:
    def __init__(self, rows, cols, total_mines):
        self._rows = rows
        self._cols = cols
        self.known = np.full((rows, cols), np.nan)
        self._total_mines = total_mines
    def known_mines_count(self):
        return np.count_nonzero(self.known == 1) # it really works!
    def known_safe_count(self):
        return np.count_nonzero(self.known == 0) # it really works also!
    def mines_left(self):
        return self._total_mines - self.known_mines_count()
    def solve(self, state):
        state = np.array([[state[y][x] if isinstance(state[y][x], int) 
                           else np.nan for x in range(self._cols)] for y in range(self._rows)])
        #the state[y][x] must be written in [y][x], not [x][y], otherwise this would cause error when combining it with self.known
        if not np.isnan(state).all():
            #transfer opened cells in state_trans, marked as 0 and append knowledge in self.known
            self.known[~np.isnan(state)] = 0 
            count_result, state = self._counting_step(state)
            if 0 in count_result:
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
        for c in range(1, num_components+1):
            result_list.append(self.guess_mine_component(state, components, c))
        # remove result_list which the size is not rows * cols, otherwise it would cause error
        try:
            for i in range(0, len(result_list)):
                j = i - 1
                if result_list[j].shape != (self._rows, self._cols):
                    del result_list[j]
        except:
            pass
        # calculate how many ~is.nan in result_list
        num_cm_neighbours = 0
        for i in range(len(result_list)):
            num_cm_neighbours += np.sum(~np.isnan(result_list[i]))
        squares_outside_cm = self._rows * self._cols - np.sum(~np.isnan(self.known)) - num_cm_neighbours
        # calculate the number of squares outside cm neighbour
        try:
            cm_mine_expected = np.sum(np.nan_to_num(result_list, copy=True))
            expected_mines = (self.mines_left() - cm_mine_expected) / squares_outside_cm
            result_list = np.sum(np.nan_to_num(result_list, copy=False), axis=0)
        except:
            expected_mines = 0
            pass
        solution_mask = np.full(np.shape(state), np.nan)
        # fill the solution_mask, first assign self.known to solution_mask, 2 = known_safe, 3 = known_mines
        solution_mask[~np.isnan(self.known)] = self.known[~np.isnan(self.known)] + 2
        # fill the solution mask, component > 0 means it's a neighbour of component, assign result_list to solution_mask
        try:
            solution_mask[components > 0] = result_list[components > 0]
            # fill the remaining nan in solution_mask with expected_mines
        except:
            pass
        self.known[solution_mask == 1] = 1
        self.known[solution_mask == 0] = 0
        solution_mask[np.isnan(solution_mask)] = expected_mines
        return solution_mask
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
                coord_neigh_cm = [(x,y) for x,y in zip(cm_neighbour[0], cm_neighbour[1])] # be careful about the order of x and y
                total_neigh_coord.append(coord_neigh_cm)
        neigh_coord_cm = set()
        for i in range(len(total_neigh_coord)):
            neigh_coord_cm = neigh_coord_cm.union(set(total_neigh_coord[i]))
        # produce a cm_index mask
        label_cm = cm.copy().astype(int) # copy cm, convert bool array to int array, otherwise we cannot assign number to cm mask
        for i in range(len(coordinate_cm)):
            (x, y) = coordinate_cm[i] #iterate tuple from coordinate_cm to map labes to label_cm
            label_cm[x,y] = i + 1
        # use constraint model to solve the problem, first add the neighbour cells to problem
        problem = Problem()
        problem.addVariables(neigh_coord_cm, [0,1])
        # add exactsumconstraint to problem, use label_cm to find the number of cm
        for i in range(len(coordinate_cm)):
            constraint = ExactSumConstraint(int(state[label_cm == i + 1]))
            problem.addConstraint(constraint, total_neigh_coord[i])
        # use maxconstraint to ensure number of mines in solutions less than remaining mines
        problem.addConstraint(MaxSumConstraint(self.mines_left()))
        solve = problem.getSolutions()
        # convert solve to a matrix, append to solutions
        solutions = []
        for i in range(len(solve)):
            M = np.full((self._rows,self._cols), np.nan)
            M[tuple(zip(*solve[i].keys()))] = list(solve[i].values())
            solutions.append(M)
        # calculate probability by sum up all the solutions, then divide by the number of solutions
        solutions = np.sum(solutions, axis = 0)/len(solutions)
        return solutions
        
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


        