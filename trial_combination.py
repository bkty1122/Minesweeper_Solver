import itertools
#https://math.stackexchange.com/questions/389619/probability-in-minesweeper reference on probability

testing_list = [[0, 0, 0, 0, 1, 'X', 2, 1, 0, 0],
                [0, 0, 0, 0, 1, 3, 'X', 3, 1, 0], 
                [0, 0, 0, 0, 0, 2, 'X', 'X', 2, 1], 
                [1, 1, 1, 0, 0, 2, 3, 3, 2, 'X'], 
                [1, 'X', 1, 0, 0, 1, 'X', 1, 1, 1], 
                [1, 1, 2, 1, 1, 1, 1, 1, 0, 0], 
                [0, 0, 2, 'X', 2, 0, 0, 1, 1, 1], 
                [0, 0, 2, 'X', 2, 0, 0, 1, 'X', 1], 
                [0, 0, 1, 1, 1, 0, 0, 1, 1, 1], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#Now the machine reveal testing_list[0][4], [1][4] and [1][5], 1,1,3
mine = set()
safe = set()

def get_neighbour(x,y):
    neighbour = []
    rows = 10
    cols = 10
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if (i,j) != (x,y) \
                and (i >= 0 and i < rows) \
                and (j >= 0 and j < cols)\
                and (i,j) not in safe:
                neighbour.append((i,j))
    return neighbour

guess_mine = []
def guess_mine_neighbour(x,y):
    neighbour = get_neighbour(x,y)
    num_mine = testing_list[x][y]
    combination =list(itertools.combinations(neighbour,num_mine))
    guess_mine.append(combination)
    return combination

guess_mine_filtered = set()
def guess_checking(x,y):
    neighbour = get_neighbour(x,y)
    num_mines = testing_list[x][y]
    guess_neighbour_same = []
    for i in guess_mine:
        for j in i:
            for k in j:
                if k in neighbour:
                    guess_neighbour_same.append(j)
    for i in guess_neighbour_same:
        if len(i) != num_mines:
            guess_neighbour_same.remove(i)
    for i in guess_mine:
        for j in i:
            if j in guess_neighbour_same:
                guess_mine_filtered.add(j)
    return guess_neighbour_same

def probability_neighbour(x,y):
    count_filtered = set()
    neighbour = set()
    neighbour_already_safe = set()
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if (i,j) in safe:
                neighbour_already_safe.add((i,j))
                neighbour.update(get_neighbour(i,j))
    neighbour_already_mine = mine.intersection(neighbour)
    check_mine_include_all = False
    for (i,j) in neighbour_already_safe:
        if testing_list[i][j] == len(neighbour_already_mine):
            check_mine_include_all = True
        else:  
            for i in guess_mine_filtered:
                for j in i:
                    if j == (x,y):
                        count_filtered.add(i)
            try:
                for i in count_filtered:
                    for j in i:
                        if (x,y) not in i:
                            count_filtered.remove(i)
            except KeyError:
                pass
    probability = len(guess_mine_filtered) / len(neighbour)
    if check_mine_include_all == True:
        probability = 0
    else:
        if probability > 1:
            probability = 1
        else:
            probability = probability
    return probability

list_trial = [[0,1],[1,2],[2,3],[3,4]]
dict_1 = {}
for i in range(len(list_trial)):
    key = tuple(list_trial[i])
    dict_1[key] = 0.1
    
print(dict_1)