import pygame, sys
from Minesweeper_gameboard import *

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 50, 50)

class Minesweeper:
    def __init__(self, row, col, mines):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(self.icon)
        self.font = pygame.font.SysFont("Arial", 15)
        self._width = 600
        self._height = 800
        self._row = row
        self._col = col
        self._mines = mines
        self.gameboard = Minesweeper_gameboard(self._row, self._col, self._mines).board
        self.playerboard = Minesweeper_playerboard(self._row, self._col, self._mines).player_board
        self.screen = pygame.display.set_mode((600, 800))
        self.clock = pygame.time.Clock()
        
    def draw_grid(self):
        """Draws the grid on the screen, the upper part show gameboard, the lower part show the control panel"""
        box_width = self._width*(0.9-0.1)/self._row
        box_height = self._height*(0.4-0.1)/self._col
        # draw grids and numbers
        for i in range(self._row):
            for j in range(self._col):
                # calculate x and y for this cell
                x = int(self._width*0.1 + i*box_width)
                y = int(self._height*0.1 + j*box_height)
                pygame.draw.rect(self.screen, white, pygame.Rect(x, y, box_width, box_height), 1)
                text = self.font.render(str(self.gameboard[i][j]), False, white)
                textRect = text.get_rect()
                textRect.center = (x+box_width//2, y+box_height//2)
                self.screen.blit(text, textRect)
        for i in range(self._row):
            for j in range(self._col):
                x = int(self._width*0.1 + i*box_width)
                y = int(self._height*0.5 + j*box_height)
                pygame.draw.rect(self.screen, white, pygame.Rect(x, y, box_width, box_height), 1)
                text = self.font.render(str(self.playerboard[i][j]), False, white)
                textRect = text.get_rect()
                textRect.center = (x+box_width//2, y+box_height//2)
                self.screen.blit(text, textRect)
        # draw title 1
        gameboard_title = self.font.render("Gameboard", False, white)
        gameboard_titleRect = gameboard_title.get_rect()
        gameboard_titleRect.center = (self._width*0.5, self._height*0.05)
        self.screen.blit(gameboard_title, gameboard_titleRect)
        # draw title 2
        playerboard_title = self.font.render("Playerboard", False, white)
        playerboard_titleRect = playerboard_title.get_rect()
        playerboard_titleRect.center = (self._width*0.5, self._height*0.45)
        self.screen.blit(playerboard_title, playerboard_titleRect)
        
    def run_game(self):
        while True:
            self.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(60)

            
if __name__ == "__main__":
    ms = Minesweeper(20,10,20)
    ms.run_game()
        