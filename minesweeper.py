import random

class Minesweeper_gameboard():
    def __init__(self, rows, cols, num_mines):
        self._rows = rows
        self._cols = cols
        self._num_mines = num_mines
        self.ADJ = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 1),(1, 0)]
        self.reset()
    def initialise(self):
        self.board = [[0 for _ in range(self._cols)] for _ in range(self._rows)]
    def add_mines(self):
        for v in random.sample(range(self._rows*self._cols), k=self._num_mines):
            row, col = divmod(v, self._cols)
            self.board[row][col] = 'X' # type: ignore
    def nearby(self):
        for row in range(self._rows):
            for col in range(self._cols):
                if self.board[row][col] != 'X':
                    for ra, ca in self.ADJ:
                        if (r := row+ra) >= 0 and r < self._rows and (c := col + ca) >= 0 and c < self._cols:
                            if self.board[r][c] == 'X':
                                self.board[row][col] += 1 # type: ignore
    def reset(self, new_mines=True): # reset the gameboard
        if new_mines:
            self.initialise()
            self.add_mines()
        else:
            for row in self._rows:
                for col in self._cols:
                    if self.board[row][col] != MINE:
                        self.board[row][col] = 0
        self.nearby()

class Minesweeper_AI():
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.move_made = set() 
        self.known_mines = set()
        self.known_safe = set()
        self.knowledge = []
    def mark_mine(self):
        count = 0 
        while count < self.num_mines:
        for i in self.knowledge:
            if i[3] >= 1:
                self.known_mines.add(i[0])
                count += 1

gameboard = Minesweeper_gameboard(10, 10, 10)
print(gameboard.board)
print(gameboard.board[0][1])

