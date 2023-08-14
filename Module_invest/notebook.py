#紀錄numpy scipy 等module 語法的用途
import numpy as np
import scipy as sp
from itertools import product
from functools import reduce
from operator import mul
from tools import *
from constraint import Problem, ExactSumConstraint

#測試 constraint module
prob = Problem()
const_exact = ExactSumConstraint(6)
prob.addVariables(['a','b','c'], [1,2,3,0,-1,4,6,-2])
prob.addConstraint(const_exact)
prob.addConstraint(lambda a, b, c: a * b * c > 1)
print('Test Problem and add Constraint set: {}'.format(prob.getSolutions()))
# Test Problem and add Constraint set: 
#     [{'a': 4, 'b': 1, 'c': 1}, {'a': 3, 'b': 2, 'c': 1}, 
#      {'a': 3, 'b': 1, 'c': 2}, {'a': 2, 'b': 3, 'c': 1}, 
#      {'a': 2, 'b': 2, 'c': 2}, {'a': 2, 'b': 1, 'c': 3}, 
#      {'a': 1, 'b': 4, 'c': 1}, {'a': 1, 'b': 3, 'c': 2}, 
#      {'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 1, 'c': 4}]

#測試 object[~np.isnan(np_nan_test_2)] = 0 的效果
np_nan_test_1 = np.full((7,7), 2)
np_nan_test_2 = np.full((7,7), np.nan)
np_nan_test_1[~np.isnan(np_nan_test_2)] = 0

#測試 & operator
and_test_1 = np.full((7,7), 2)
and_test_2 = np.full((1,7), 3)
and_test_3 = np.isnan(and_test_2)
and_operater_test = and_test_3 & and_test_2

#測試 dict properties, enumerate
dict_trial = {(0,2):{1: 0.3, 2: 0.4}, (0,4):{1: 0.4, 2: 0.3}}
product_trial = product(*[d for d in dict_trial])
#print out (with *): [(0, 0), (0, 4), (2, 0), (2, 4)]
#without *: ([(0, 2), (0, 4)])[((0, 2),), ((0, 4),)]
enumerate_trial = []
for a in product_trial:
    print(sum(a))
    enumerate_trial.append(sum(a))
    print(list(enumerate(enumerate_trial)))
    #output: 0, 4, 2, 6, (0 + 0) = 0, (0 + 4) = 4, (2 + 0) = 2, (2 + 4) = 6
    #output for enumerate result: [(0, 0), (1, 4), (2, 2), (3, 6)]

#Test reduce module and np.add
print('testinf result of reduce: {}'\
    .format(reduce(np.add, enumerate(enumerate_trial))))
#壓縮至(x,y), x = 0 + 1 + 2 + 3 = 6, y = 0 + 4 + 2 + 6 = 12

mul_trial = [[1,2,3,4], [2,3,4,5]]
print('testing result of mul and reduce: {}'\
    .format(reduce(mul, [mul_trial[i][j] for i in range(len(mul_trial)) for j in range(i)])))

#Test lambda usage
lambda_list = [[1,2,3],[4,5],[-1,-2], [-1, 0, 1]]
lambda_trial = list(filter(lambda x: sum(x) > 0, lambda_list))
print(lambda_trial)
#output: [[1, 2, 3], [4, 5]]
lambda_list_1 = [[1,2],[2,3], [3,4], [-1,-2], [0, -1, -2, -3]]
lambda_trial_1_result = []
for i in range(len(lambda_list_1)):
    lambda_trial_1 = reduce(lambda x, y : x * y, lambda_list_1[i])
    lambda_trial_1_result.append(lambda_trial_1)
print(lambda_trial_1_result)

#unused code
        # k = 1
        # while k < (len(solutions)):
        #     j = 0
        #     j_k_interset = ~np.isnan(solutions[j]) & ~np.isnan(solutions[k])
        #     j_k_bool_interset = boolean_combine(solutions[j], j_k_interset)
        #     j_k_test = np.nan_to_num(j_k_bool_interset, copy = False) == np.nan_to_num(solutions[k], copy = False)
        #     if j_k_test.all() == True:
        #        del solutions[j]
        #        k -= 1
        #     k += 1
        
        # # build a mask for each label_cm, calculate prob for mines in each cells
        # prob_semi = []
        # cm_index_check = 1
        # while cm_index_check < np.count_nonzero(label_cm) + 1:
        #     j_list = []
        #     for j in range(len(solutions)):
        #         if solutions[j][0] == cm_index_check:
        #             j_list.append(j)
        #     j_array = [solutions[j][1:] for j in j_list]
        #     j_array = np.sum(np.nan_to_num(j_array, copy = False), axis = 0)
        #     j_array = j_array/len(j_list)
        #     j_array = np.array(j_array).astype(float)
        #     j_array[j_array == 0] = np.nan
        #     j_array = [i for s in j_array for i in s]
        #     j_array = [i for s in j_array for i in s]
        #     j_array = [i for s in j_array for i in s]
        #     j_array = np.array(j_array).reshape(self._rows, self._cols)
        #     prob_semi.append(j_array)
        #     cm_index_check += 1
        # # now, prob is a list of arrays. each array is a probability matrix for each cm
        # # prob[0] is the probability matrix for cm 1, prob[1] is the probability matrix for cm 2, etc.
        # # compare different non-zero element, choose the one with the highest probability;
        
        
        
        #         prob_semi = []
        # cm_index_check = 1
        # while cm_index_check < np.count_nonzero(label_cm) + 1:
        #     j_list = []
        #     for j in range(len(solutions)):
        #         if solutions[j][0] == cm_index_check:
        #             j_list.append(j)
        #     j_array = [solutions[j][1:] for j in j_list]
        #     j_array = np.sum(np.nan_to_num(j_array, copy = False), axis = 0)
        #     j_array = j_array/len(j_list)
        #     j_array = [i for s in j_array for i in s]
        #     prob_semi.append(j_array)
        #     cm_index_check += 1
        # # now, prob is a list of arrays. each array is a probability matrix for each cm
        # # prob[0] is the probability matrix for cm 1, prob[1] is the probability matrix for cm 2, etc.
        # # compare different non-zero element, choose the one with the highest probability;
        # for i in prob_semi:
        #     print(i)
        # # solutions = [solutions[i][1:] for i in range(len(solutions))]
        
[[       nan        nan        nan        nan        nan        nan nan]
 [       nan        nan        nan        nan        nan        nan nan]
 [       nan        nan        nan        nan        nan        nan nan]
 [       nan        0.16666667 0.25       0.25       0.41666667 nan nan]
 [       nan        0.16666667 2.         2.         0.41666667 nan nan]
 [       nan        0.16666667 nan        0.         0.41666667 nan nan]
 [       nan        0.         2.         0.         nan        nan nan]]

array([[       nan,        nan,        nan, 0.4       , 0.2       , 0.2       , 0.06666667],
       [       nan,        nan,        nan, 0.4       ,        nan, nan, 0.06666667],
       [       nan,        nan,        nan, 0.4       , 0.2       , 0.2       , 0.06666667],
       [       nan,        nan,        nan,        nan,        nan, nan,        nan],
       [       nan,        nan,        nan,        nan,        nan, nan,        nan],
       [       nan,        nan,        nan,        nan,        nan, nan,        nan],
       [       nan,        nan,        nan,        nan,        nan, nan,        nan]])

[[1, 1, 1, 1, 1, 0, 0], 
['X', 1, 1, 'X', 2, 1, 1], 
[1, 1, 1, 1, 2, 'X', 1], 
[0, 0, 0, 1, 2, 2, 1], 
[0, 1, 2, 3, 'X', 1, 0], 
[0, 1, 'X', 'X', 3, 2, 1], 
[0, 1, 2, 2, 2, 'X', 1]]