import random, itertools

class Minesweeper_gameboard():
    def __init__(self, rows, cols, num_mines):
        self._rows = rows
        self._cols = cols
        self._num_mines = num_mines
        self.ADJ = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 1),(1, 0)]
        self.MINE = 'X'
        self.FLAG = 'F'
        self.reset()
    def initialise(self):
        self.board = [[0 for _ in range(self._cols)] for _ in range(self._rows)]
    def add_mines(self):
        for v in random.sample(range(self._rows*self._cols), k=self._num_mines):
            row, col = divmod(v, self._cols)
            self.board[row][col] = self.MINE # type: ignore
    def nearby(self):
        for row in range(self._rows):
            for col in range(self._cols):
                if self.board[row][col] != self.MINE:
                    for ra, ca in self.ADJ:
                        if (r := row+ra) >= 0 and r < self._rows and (c := col + ca) >= 0 and c < self._cols:
                            if self.board[r][c] == self.MINE:
                                self.board[row][col] += 1 # type: ignore
    def reset(self, new_mines=True): # reset the gameboard
        if new_mines:
            self.initialise()
            self.add_mines()
        else:
            for row in self._rows:
                for col in self._cols:
                    if self.board[row][col] != self.MINE:
                        self.board[row][col] = 0
        self.nearby()

class Minesweeper_playerboard():
    def __init__(self, rows, cols, num_mines):
        self._rows = rows
        self._cols = cols
        self.num_mines = num_mines
        self.player_board_init()
    def player_board_init(self):
        self.player_board = [['-' for _ in range(self._cols)] for _ in range(self._rows)]
    def count_string(self, object, count_string):
        object_flat_1 = [a for c in object for a in c]
        object_flat_2 = [a for c in object_flat_1 for a in c]
        #since the gameboard is a triple list, need to flattening it twice
        y = object_flat_2.count(count_string)
        return y
    def winning(self):
        if self.count_string(self.player_board,'-') == 0:
            return True
        return False
    def lose(self):
        if self.count_string(self.player_board,'X') > 0:
            return True
        return False

class Minesweeper_AI():
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.move_made = set() 
        self.known_mines = set()
        self.known_safe = set()
        self.guess_mine = []
        self.guess_mine_filtered = set()
        self.neighbour_general = set()
        self.player_board = playerboard.player_board.copy()
    def get_neighbour(self, x, y):
        neighbour = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i >= 0 and i < self.rows) \
                and (j >= 0 and j < self.cols) \
                and (i, j) != (x, y) \
                and (i, j) not in self.known_safe:
                    neighbour.append((i,j))
                    self.neighbour_general.add((i,j))
        return neighbour
    def guess_mine_neighbour(self,x,y):
        neighbour = self.get_neighbour(x,y)
        num_mine = self.player_board[x][y]
        combination =list(itertools.combinations(neighbour,num_mine))
        self.guess_mine.append(combination)
        return combination
    def guess_checking(self,x,y):
        neighbour = self.get_neighbour(x,y)
        num_mines = self.player_board[x][y]
        guess_neighbour_same = []
        for i in self.guess_mine:
            for j in i:
                for k in j:
                    if k in neighbour:
                        guess_neighbour_same.append(j)
        for i in guess_neighbour_same:
            if len(i) != num_mines:
                guess_neighbour_same.remove(i)
        for i in self.guess_mine:
            for j in i:
                if j in guess_neighbour_same:
                    self.guess_mine_filtered.add(j)
        return guess_neighbour_same
    def probability_neighbour(self,x,y):
        count_filtered = set()
        neighbour = set()
        neighbour_already_safe = set()
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if (i,j) in self.known_safe:
                    neighbour_already_safe.add((i,j))
                    neighbour.update(self.get_neighbour(i,j))
        neighbour_already_mine = self.known_mines.intersection(neighbour)
        check_mine_include_all = False
        for (i,j) in neighbour_already_safe:
            if self.player_board[i][j] == len(neighbour_already_mine):
                check_mine_include_all = True
            else:  
                for i in self.guess_mine_filtered:
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
        probability = len(self.guess_mine_filtered) / len(neighbour)
        if check_mine_include_all == True:
            probability = 0
        else:
            if probability > 1:
                probability = 1
            else:
                probability = probability
        return probability
    def probability_not_neighbour(self,x,y):
        for x in self.player_board:
            for y in x:
                if (x,y) not in self.neighbour_general:
                    probability = (self.num_mines - len(self.known_mines))\
                                /(self.rows * self.cols - len(self.known_safe)\
                                - len(self.neighbour_general))
                    return probability
    def get_all_probability(self):
        cell_probability = {}
        for x in self.player_board:
            for y in x:
                if (x,y) not in self.neighbour_general:
                    key = tuple(self.player_board[x])
                    cell_probability[key] = self.probability_not_neighbour(x,y)
                else:
                    key = tuple(self.player_board[x])
                    cell_probability[key] = self.probability_neighbour(x,y)
        return cell_probability
    def make_safe_move(self):
        cell_probability = self.get_all_probability()
        for (i,j) in cell_probability:
            if cell_probability[(i,j)] == 0:
                self.known_safe.add((i,j))
                return (i,j)
            elif min(cell_probability.values()) > 0 and len(self.known_safe) == 0:
                return random.choice(min(cell_probability, key=cell_probability.get))
        return None, None
    def mark_mine(self):
        cell_probability = self.get_all_probability()
        if min(cell_probability.values()) == 0 and len(self.known_safe) == 0:
            return max(cell_probability, key=cell_probability.get)
        return None, None
    def make_move(self):
        (i,j) = self.make_safe_move
        playerboard.player_board[i][j] = gameboard.board[i][j]
        self.known_safe.add(i,j)
        (x,y) = self.mark_mine()
        playerboard.player_board[x][y] = 'F'
        self.known_mines.add(x,y)
        print(playerboard.player_board)
        
        

rols = 10
cols = 10
mines = 10

playerboard = Minesweeper_playerboard(rols, cols, mines)
gameboard = Minesweeper_gameboard(rols, cols, mines)
MinesweeperAI_bot = Minesweeper_AI(rols,cols,mines)

print(playerboard.player_board)

print(MinesweeperAI_bot.get_all_probability())