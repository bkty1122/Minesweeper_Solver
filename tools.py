#Ref: https://github.com/JohnnyDeuss/minesweeper-solver/blob/master/minesweeper_solver/solver.py
import numpy as np
from scipy.ndimage import binary_dilation
from scipy.ndimage import generate_binary_structure
from scipy.signal import convolve2d

def dilate(bool_ar):
    """ Perform binary dilation 擴張 with a structuring element with connectivity 2. """
    return binary_dilation(bool_ar, structure=generate_binary_structure(2, 2))

def neighbors(bool_ar):
    """ Return a binary mask marking all squares that neighbor a True cells in the boolean array. """
    return bool_ar ^ dilate(bool_ar)

def neighbors_xy(x, y, shape):
    """ Return a binary mask marking all squares that neighbor the square at (x, y). """
    return neighbors(mask_xy(x, y, shape))

def mask_xy(x, y, shape):
    """ Create a binary mask that marks only the square at (x, y). """
    mask = np.zeros(shape, dtype=bool)
    mask[y, x] = True
    return mask

def boundary(state):
    """ Return a binary mask marking all closed squares that are adjacent to a number. """
    return neighbors(~np.isnan(state))

def count_neighbors(bool_ar):
    """ Calculate how many True's there are next to a square. """
    filter = np.ones((3, 3))
    filter[1, 1] = 0
    return convolve2d(bool_ar, filter, mode='same')

def reduce_numbers(state, mines=None):
    """ Reduce the numbers in the state to represent the number of mines next to it that have not been found yet.
        :param state: The state of the minefield.
        :param mines: The mines to use to reduce numbers
    """
    num_neighboring_mines = count_neighbors(mines)
    state[~np.isnan(state)] -= num_neighboring_mines[~np.isnan(state)]
    return state

def boolean_combine(arr_a, arr_bool):
        combined = []
        for row_a, row_b in zip(arr_a, arr_bool):
            row_combined = []
            for a, b in zip(row_a, row_b):
                if a == 'True':
                    row_combined.append(b)
            else:
                row_combined.append(a)
                combined.append(np.asarray(row_combined))
        return np.asarray(combined)

def overlap_compare_replace(state, label, x, y, prob, result):
    '''
    Compare two prob results, return the prob in which is larger. modify the smaller results.
    '''
    equal = False
    x_y_overlap = ~np.isnan(prob[x][0]) & ~np.isnan(prob[y][0]) # True if overlap
    x_not_overlap = ~x_y_overlap & ~np.isnan(prob[x][0])
    y_not_overlap = ~x_y_overlap & ~np.isnan(prob[y][0])
    if x_y_overlap.any() == True:
        if (prob[x][0][x_y_overlap] > prob[y][0][x_y_overlap]).any():
            if prob[y][0][x_y_overlap].sum() == 0:
                prob[x][0][x_not_overlap] = (int(state[label == x + 1]) - result[x_y_overlap].sum())/ x_not_overlap.sum()
                result[x_not_overlap] = prob[x][0][x_not_overlap]
            else:
                result[x_y_overlap] = prob[x][0][x_y_overlap]
                prob[y][0][x_y_overlap] = 0
                prob[y][0][y_not_overlap] = (int(state[label == y + 1]) - result[x_y_overlap].sum())/ y_not_overlap.sum()
        if (prob[x][0][x_y_overlap] < prob[y][0][x_y_overlap]).any():
            if prob[x][0][x_y_overlap].sum() == 0:
                prob[y][0][y_not_overlap] = (int(state[label == y + 1]) - result[x_y_overlap].sum())/ y_not_overlap.sum()
                result[y_not_overlap] = prob[y][0][y_not_overlap]
            else:
                result[x_y_overlap] = prob[y][0][x_y_overlap]
                prob[x][0][x_y_overlap] = 0
                prob[x][0][x_not_overlap] = (int(state[label == x + 1]) - result[x_y_overlap].sum())/ x_not_overlap.sum()
        else:
            equal = True
            return prob, result
    # check whether prob has turn to result
    if equal == False:
        x_result_notinclude = np.isnan(result) & ~np.isnan(prob[x][0])
        y_result_notinclude = np.isnan(result) & ~np.isnan(prob[y][0])
        if x_result_notinclude.any():
            result[x_result_notinclude] = prob[x][0][x_result_notinclude]
        if y_result_notinclude.any():
            result[y_result_notinclude] = prob[y][0][y_result_notinclude]
    return prob, result