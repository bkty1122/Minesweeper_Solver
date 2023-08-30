import pygame, sys
from Minesweeper_gameboard import *
from Minesweeper_solver import *
from tools import count_string
from button import game_button

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 50, 50)
lightgrey = (105, 105, 105)
sprites = pygame.sprite.Group()

class Minesweeper:
    def __init__(self, row, col, mines):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(self.icon)
        self.font = pygame.font.SysFont("Arial", 20)
        self._width = 800
        self._height = 800
        self._row = row
        self._col = col
        self._mines = mines
        self.box_width = self._width*(0.9-0.1)/self._row
        self.box_height = self._height*(0.9-0.1)/self._col
        self.gameboard = Minesweeper_gameboard(self._row, self._col, self._mines).board
        self.playerboard = Minesweeper_playerboard(self._row, self._col, self._mines).player_board
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse.get_pos()
        
    def winning(self):
        count_unknown = count_string(self.playerboard, '-')
        if count_unknown == 0:
            print('Winning')
            return True
        return False
    
    def losing(self):
        count_mine = count_string(self.playerboard, 'X')
        if count_mine > 0:
            print('Losing')
            return True
        return False
    
    def playerboard_title(self):
        # draw title of playerboard
        playerboard_title = self.font.render("Playerboard", False, white)
        playerboard_titleRect = playerboard_title.get_rect()
        playerboard_titleRect.center = (self._width*0.5, self._height*0.05)
        self.screen.blit(playerboard_title, playerboard_titleRect)
        for i in range(self._row):
            for j in range(self._col):
                x = int(self._width*0.1 + i* self.box_width)
                y = int(self._height*0.1 + j* self.box_height)
                pygame.draw.rect(self.screen, white, pygame.Rect(x, y, self.box_width, self.box_height), 1)
    
    def draw_playerboard_computer(self):
        for i in range(self._row):
            for j in range(self._col):
                x = int(self._width*0.1 + i* self.box_width)
                y = int(self._height*0.1 + j* self.box_height)
                text = self.font.render(str(self.playerboard[i][j]), False, white)
                textRect = text.get_rect()
                textRect.center = (x+ self.box_width //2, y + self.box_height //2)
                self.screen.blit(text, textRect)
                
    def solver_test(self):
        ms = Minesweeper_solver(self._row, self._col, self._mines)
        solve_result = ms.solve(self.playerboard)
        for i in range(self._row):
            for j in range(self._col):
                if ms.known[i][j] == 1:
                    self.update_playerboard((i,j), 'F', red)
        min = np.nanmin(solve_result)
        y, x = np.where(solve_result == min)
        coord = list(zip(y, x))
        if len(coord) > 0:
            coord = random.choice(coord)
        self.update_playerboard(coord)
        if self.playerboard[coord[0]][coord[1]] == 'X':
            print('Mine location:{}, Loss rate: {}'.format(coord, min))
        else:
            ms.known[coord[0]][coord[1]] = 0
        
    def update_playerboard(self, coord, value = None, color = white):
        '''
        Eliminate the box and update the number, otherwise the board would be ugly :>
        '''
        i = coord[0]
        j = coord[1]
        x = int(self._width*0.1 + i* self.box_width)
        y = int(self._height*0.1 + j* self.box_height)
        if value is not None:
            self.playerboard[i][j] = value
        else:
            self.playerboard[i][j] = self.gameboard[i][j]
        text = self.font.render(str(self.playerboard[i][j]), True, color)
        textRect = text.get_rect()
        textRect.center = (x + self.box_width//2, y + self.box_height//2)
        self.screen.fill(black, (x + (self.box_width * 0.2), y + (self.box_height * 0.2), self.box_width * 0.8, self.box_height * 0.8))
        self.screen.blit(text, textRect)         
    def draw_playerboard_human(self):
        for i in range(self._row):
            for j in range(self._col):
                x = int(self._width* 0.1 + i* self.box_width)
                y = int(self._height* 0.1 + j* self.box_height)
                sprites.add(game_button(black, white, lightgrey, white, pygame.Rect(x, y, self.box_width, self.box_height)
                                        ,i, j, self.playerboard, self.gameboard, white))
    
    def run_game(self, solver = False):
        if solver == False:
            self.draw_playerboard_human()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            # if the mouse leave the square, remain normal color
            self.playerboard_title()
            if solver == False:
                sprites.update(events)
                sprites.draw(self.screen)
            else:
                self.draw_playerboard_computer()
                self.solver_test()
            pygame.display.flip()
            self.clock.tick(30)
            
            if self.winning() == True or self.losing() == True:
                break

if __name__ == "__main__":
    ms = Minesweeper(20,20,40)
    while ms.losing() == False and ms.winning() == False:
        ms.run_game(solver = False)