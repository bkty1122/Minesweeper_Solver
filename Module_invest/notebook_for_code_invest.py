'''
This is to investigate the methology behind the Minesweeper_AI code. 
I've figure out the methology of Minesweeper solver on paper, now investigating how to convert the methology
into code.
'''

state = np.full((7,7), np.nan)
state[0,0] = 1
state[1,1] = 1
state[2,2] = 1
known = np.full((7,7), np.nan)
a = np.isnan(known) & boundary(state)
b = np.isnan(known)& ~a & np.isnan(state)
n = b.sum(dtype = int)
# print(b)
# print(n)
# output:
# b = 
# [[False False False  True  True  True  True]
#  [False False False False  True  True  True]
#  [False False False False  True  True  True]
#  [ True False False False  True  True  True]s
#  [ True  True  True  True  True  True  True]
#  [ True  True  True  True  True  True  True]
#  [ True  True  True  True  True  True  True]]
# n =
# 35, which are the total number of 'True' in b
c = dilate(np.isnan(state) & np.isnan(known)) & ~np.isnan(state)
# print(c)
# output:
# [[ True False False False False False False]
#  [False  True False False False False False]
#  [False False  True False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]
#  [False False False False False False False]]
d,e = label(c)
# print(d)
# print(e)
# output:
# d = 
# [[1 0 0 0 0 0 0]
#  [0 2 0 0 0 0 0]
#  [0 0 3 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]]
# e = 3
number_boundary_masks = [neighbors(d == i) & np.isnan(known) & np.isnan(state) for i in range(1, e+1)]
for i in range(len(number_boundary_masks)):
    print(number_boundary_masks[i].astype(int))
# output:
# [[0 1 0 0 0 0 0]
#  [1 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]]
# [[0 1 1 0 0 0 0]
#  [1 0 1 0 0 0 0]
#  [1 1 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]]
# [[0 0 0 0 0 0 0]
#  [0 0 1 1 0 0 0]
#  [0 1 0 1 0 0 0]
#  [0 1 1 1 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]
#  [0 0 0 0 0 0 0]]
