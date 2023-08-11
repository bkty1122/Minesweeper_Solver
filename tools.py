""" A module with common functions for working with minesweeper games. """
import numpy as np
from scipy.ndimage import binary_dilation
#https://zhuanlan.zhihu.com/p/362042756 binary_dilation 的用途
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

# print(neighbors_xy(0,0,(7,7)))
# in the tool pack, input neighbours_xy, return array that only mark 
# cells that are neighbour to (x,y) as 'True'
# output: 
# [[False  True False False False False False]
#  [ True  True False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]]

def mask_xy(x, y, shape):
    """ Create a binary mask that marks only the square at (x, y). """
    mask = np.zeros(shape, dtype=bool)
    mask[y, x] = True
    return mask

def boundary(state):
    """ Return a binary mask marking all closed squares that are adjacent to a number. """
    return neighbors(~np.isnan(state))
# state = np.full((7,7), np.nan)
# state[0,0] = 1
# state[1,1] = 1
# print(state & boundary(state))
# State output: 
# [[ 1. nan nan nan nan nan nan]
#  [nan  1. nan nan nan nan nan]
#  [nan nan nan nan nan nan nan]
#  [nan nan nan nan nan nan nan]
#  [nan nan nan nan nan nan nan]
#  [nan nan nan nan nan nan nan]
#  [nan nan nan nan nan nan nan]]
# under this state, the boundary module produce the following output:
# [[False  True  True False False False False]
#  [ True False  True False False False False]
#  [ True  True  True False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]]
# True means arrays involue in the guessing state (known in its neighbour), 
# False means arrays not involved in the guessing state

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

def boolean_combine(arr_a, arr_b):
        combined = []
        for row_a, row_b in zip(arr_a, arr_b):
            row_combined = []
            for a, b in zip(row_a, row_b):
                if a == 'True':
                    row_combined.append(b)
            else:
                row_combined.append(a)
                combined.append(np.asarray(row_combined))
        return np.asarray(combined)

# array([[ True,  True,  True, False, False, False,  True],
#        [ True,  True,  True, False,  True, False,  True],
#        [ True,  True,  True, False, False, False,  True],
#        [ True, False, False, False,  True,  True,  True],
#        [ True, False,  True, False,  True,  True,  True],
#        [ True, False, False, False,  True,  True,  True],
#        [ True,  True,  True,  True,  True,  True,  True]])))