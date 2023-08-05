import random
import numpy as np

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
        #since the gameboard is a triple list, need to flattening it twice
        y = object_flat_1.count(count_string)
        return y
    def winning(self):
        if self.count_string(self.player_board,'-') == 0\
            or self.count_string(self.player_board,'-') == self.num_mines:
            return True
        return False
    def lose(self):
        if self.count_string(self.player_board,'X') > 0:
            return True
        return False

class Sentences():
    # would return {cell} = count, if print it by a for loop
    def __init__(self, cell, count):
        self.cell = set(cell)
        self.count = count
    def __eq__(self, other):
        return self.cell == other.cell and self.count == other.count
    def __str__(self):
        return f'({self.cell}) = {self.count}'
    def known_mine(self):
        if len(self.cell) == self.count:
            return self.cell
        return None
    def known_safe(self):
        if self.count == 0:
            return self.cell
    def mark_mine(self, cell):
        if cell in self.cell:
            self.cell.remove(cell)
            self.count -= 1
    def mark_safe(self, cell):
        if cell in self.cell:
            self.cell.remove(cell)
    
class Minesweeper_AI():
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.move_made = set() 
        self.mines = set()
        self.safe = set()
        self.knowledge = []
        #list 可以存下class object and function, 不會只限數字/字串
        self.player_board = playerboard.player_board
    def get_neighbour(self, cell, count):
        (x,y) = cell
        neighbour = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i >= 0 and i < self.rows) \
                and (j >= 0 and j < self.cols) \
                and (i, j) != (x, y) \
                and (i, j) not in self.move_made\
                and (i,j) not in self.safe\
                and (i,j) not in self.mines:
                    neighbour.append((i,j))
                if (i,j) in self.mines:
                    count -= 1
        return neighbour, count
    def mark_mine(self, cell):
        self.mines.add(cell)
        for s in self.knowledge:
            s.mark_mine(cell)
            self.player_board[cell[0]][cell[1]] = 'F'
    def mark_safe(self, cell):
        self.safe.add(cell)
        #naming the function name as the same as knowledge to compare knowledge and update knowledge
        for s in self.knowledge:
            s.mark_safe(cell)
    def add_knowledge(self, cell, count):
        self.mark_safe(cell)
        self.move_made.add(cell)
        neighbour, count = self.get_neighbour(cell,count)
        
        sentence = Sentences(neighbour,count)
        self.knowledge.append(sentence)
        
        extend_knowledge = []
        for s in self.knowledge:
            if s == sentence:
                continue
            elif s.cell.issubset(sentence.cell):
                diff = s.cell - sentence.cell
                #對比兩個cell 之間的地雷數量差別，如果差別等於diff_count，則diff是地雷；如果差別等於0，則diff是安全的
                #如果差別不等於0或diff_count，則將差別加入extend_knowledge
                if s.count == sentence.count:
                    for cell in diff:
                        self.mark_safe(cell)
                elif len(diff) == s.count - sentence.count:
                    for cell in diff:
                        self.mark_mine(cell)
                else:
                    extend_knowledge.append(Sentences(diff,s.count - sentence.count))
            elif sentence.cell.issubset(s.cell):
                diff = sentence.cell - s.cell
                if s.count == sentence.count:
                    for cell in diff:
                        self.mark_safe(cell)
                elif len(diff) == sentence.count - s.count:
                    for cell in diff:
                        self.mark_mine(cell)
                else:
                    extend_knowledge.append(Sentences(diff,sentence.count - s.count))
            self.knowledge.extend(extend_knowledge)
            #不可以用append, 不然list 會變成：[ABC, [append_knowledge]]
            self.remove_duplicate()
            self.remove_sures
    def remove_duplicate(self):
        unique_knowledge = []
        for s in self.knowledge:
            if s not in unique_knowledge:
                unique_knowledge.append(s)
        self.knowledge = unique_knowledge
    def remove_sures(self):
        final_knowledge = []
        for s in self.knowledge:
            final_knowledge.append(s)
            if s.mark_mines():
                for mineFound in s.known_mines():
                    self.mark_mine(mineFound)
                final_knowledge.pop(-1)
            elif s.known_safes():
                for safeFound in s.known_safes():
                    self.mark_safe(safeFound)
                final_knowledge.pop(-1)
                # pop 代表刪除list 裏的資料，-1代表最後一個，pop(-1)代表刪除list 裏最後一個array
        self.knowledge = final_knowledge
    def make_random_move(self):
        all_move = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) not in self.mines and (i,j) not in self.move_made:
                    all_move.add((i,j))
        if len(all_move) == 0:
            return None
        else:
            return random.choice(tuple(all_move))
    def make_safe_move(self):
        safe_move = self.safe - self.move_made
        if len(safe_move) == 0:
            return None
        return safe_move.pop()
    def make_move(self):
        while playerboard.winning() is False and playerboard.lose() is False:
            print(self.mines)
            print(self.safe)
            print(self.move_made)
            if self.make_safe_move() is None:
                (x,y) = self.make_random_move()
                self.player_board[x][y] = gameboard.board[x][y]
                print(self.player_board)
            else:
                (x,y) = self.make_safe_move()
                self.player_board[x][y] = gameboard.board[x][y]
                print(self.player_board)
            if isinstance(gameboard.board[x][y],int) is True:
                self.add_knowledge((x,y),gameboard.board[x][y])
        if playerboard.winning() is True:
            print('You win!')
        elif playerboard.lose() is True:
            print('You lose!')
            
rols = 7
cols = 7
mines = 7

playerboard = Minesweeper_playerboard(rols, cols, mines)
gameboard = Minesweeper_gameboard(rols, cols, mines)
MinesweeperAI_bot = Minesweeper_AI(rols,cols,mines)

print(gameboard.board)
