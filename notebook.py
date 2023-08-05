#紀錄numpy scipy 等module 語法的用途
import numpy as np
import scipy as sp
from itertools import product
from functools import reduce
from operator import mul

#測試 object[~np.isnan(np_nan_test_2)] = 0 的效果
np_nan_test_1 = np.full((7,7), 2)
np_nan_test_2 = np.full((7,7), np.nan)
np_nan_test_1[~np.isnan(np_nan_test_2)] = 0

#測試 & operator
and_test_1 = np.full((7,7), 2)
and_test_2 = np.full((1,7), 3)
and_test_3 = np.isnan(and_test_2)
and_operater_test = and_test_3 & and_test_2
print(and_operater_test.sum(dtype=int))

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
    reduce(np.add, enumerate(enumerate_trial)))
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

