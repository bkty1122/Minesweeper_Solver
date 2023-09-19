import pygame, sys, io
from urllib.request import urlopen
from Minesweeper_gameboard import *
from Minesweeper_solver import *
from tools import count_string
from button import game_button, general_button

# https://pythonprogramming.net/pygame-button-function-events/

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 50, 50)
lightgrey = (105, 105, 105)
sprites_playerboard = pygame.sprite.Group()
sprites_selector = pygame.sprite.Group()

icon_url = "https://upload.wikimedia.org/wikipedia/commons/2/26/Minesweeper_start_Kmine.png"
icon = io.BytesIO(urlopen(icon_url).read())

class Minesweeper:
    def __init__(self, row, col, mines):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.icon = pygame.image.load(icon)
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
            return True
        return False
    def losing(self):
        count_mine = count_string(self.playerboard, 'X')
        if count_mine > 0:
            return True
        return False
    
    def playerboard_title(self):
        # draw title of playerboard
        playerboard_title = self.font.render("Playerboard", False, white)
        playerboard_titleRect = playerboard_title.get_rect()
        playerboard_titleRect.center = (self._width*0.5, self._height*0.05)
        self.screen.blit(playerboard_title, playerboard_titleRect)
        # draw girds for the board
        for i in range(self._row):
            for j in range(self._col):
                x = int(self._width*0.1 + i* self.box_width)
                y = int(self._height*0.1 + j* self.box_height)
                pygame.draw.rect(self.screen, white, pygame.Rect(x, y, self.box_width, self.box_height), 1)
    def selector(self):
        selector_computer = 'Solve by computer'
        selector_human = 'Solve by human'
        global selector_computer_rect, selector_human_rect
        selector_computer_rect = pygame.Rect(0, 0, len(selector_computer) * 10, 30)
        selector_human_rect = pygame.Rect(0, 30, len(selector_human) * 10, 30)
        sprites_selector.add(
            general_button(black, lightgrey, white, selector_computer_rect, 
                           lambda: print('computer'), selector_computer, 'clicked', True, white)
        )
        sprites_selector.add(
            general_button(black, lightgrey, white, selector_human_rect,
                           lambda: print('human'), selector_human, 'clicked', True, white)
        )
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
                sprites_playerboard.add(game_button(black, white, lightgrey, white, pygame.Rect(x, y, self.box_width, self.box_height)
                                        ,i, j, self.playerboard, self.gameboard, white))
    def run_game_selector(self):
        self.playerboard_title()
        self.selector()
        run_game = False
        solver = False
        while run_game == False:
            events = pygame.event.get()
            self.mouse = pygame.mouse.get_pos()
            # events 要在 while loop 裏面，不然program 不會 detect 到 event...
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and selector_human_rect.collidepoint(self.mouse):
                    run_game = True
                    solver = False
                elif event.type == pygame.MOUSEBUTTONDOWN and selector_computer_rect.collidepoint(self.mouse):
                    run_game = True
                    solver = True
            sprites_selector.update(events)
            sprites_selector.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)
        while run_game == True:
            self.run_game(solver)
    def run_game(self, solver):
        if solver == False:
            self.draw_playerboard_human()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            if solver == False:
                sprites_playerboard.update(events)
                sprites_playerboard.draw(self.screen)
            else:
                self.draw_playerboard_computer()
                self.solver_test()
            pygame.display.flip()
            self.clock.tick(30)
            if self.losing() == True or self.winning() == True:
                sys.exit()
                
if __name__ == "__main__":
    ms = Minesweeper(20,20,100)
    while ms.losing() == False and ms.winning() == False:
        ms.run_game_selector()