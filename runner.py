import random
from Minesweeper_solver import *

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