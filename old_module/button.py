import pygame.font

White = (255, 255, 255)
Black = (0, 0, 0)
Grey = (128, 128, 128)
Lightgrey = (211, 211, 211)
font = pygame.font.SysFont("Arial", 20)

class general_button:
    def __init__(self, x, y, width, height, buttontext = 'Button', normalcolor, hovercolor, retainedcolor, boundarycolor, function = None,
                 retainstatus = False, screen = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttontext = buttontext
        self.function = function
        self.normalColor = normalcolor
        self.hoverColor = hovercolor
        self.retainedColor = retainedcolor
        self.boundaryColor = boundarycolor
        self.mouse = pygame.mouse.get_pos()
        self.buttonsurface = pygame.Surface((self.width, self.height)) # create image box
        self.buttonsurf = font.render(self.buttontext, True, (20, 20, 20))
        self.buttonrect = pygame.Rect(self.x, self.y, self.width, self.height) #create rectangle for the button
        self.screen = screen
        self.already_pressed = False
        self.retainstatus = retainstatus

    def putbutton(self):
        self.buttonsurface.fill(self.normalColor)
        if self.buttonrect.collidepoint(self.mouse):
            self.buttonsurface.fill(self.hoverColor)
        elif self.already_pressed == True:
            self.buttonsurface.fill(self.retainedColor)
            
        self.buttonsurface.blit(self.buttonsurf, [self.buttonrect.width/2 - self.buttonsurf.get_rect().width/2, 
                            self.buttonrect.height/2 - self.buttonsurf.get_rect().height/2
                            ])
        self.screen.blit(self.buttonsurface, self.buttonrect)
        pygame.draw.rect(self.screen, self.boundaryColor, self.buttonrect, 1)

    def animation(self):
        general_button.putbutton(self)
        if self.retainstatus == True:
            if pygame.mouse.get_pressed(num_buttons=3)[0] and self.already_pressed == False:
                self.function()
                self.already_pressed = True
            elif pygame.mouse.get_pressed(num_buttons=3)[0] and self.already_pressed == True:
                print('already pressed')
        else:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.function()

#  Class Minesweeper_gameboard to create the gameboard
class gamebutton():
    def __init__(self, x, y, i, j, width, height, playerboard, gameboard, screen):
        # x and y equal to location of button
        self.x = x
        self.y = y
        # i and j equal to location of gameboard
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self.playerboard = playerboard
        self.gameboard = gameboard
        self.screen = screen
        self.is_flagged = False
        self.is_clicked = False
        self.mouse = pygame.mouse.get_pos()
        self.buttonsurface = pygame.Surface((self.width, self.height))
        self.buttonrect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.normalColor = Grey
        self.hoverColor = Lightgrey
        self.retainedColor = Lightgrey
        self.boundaryColor = White

    def putbutton(self):
        i = self.i
        j = self.j
        buttontext = str(self.playerboard[i][j])
        buttonsurf = font.render(buttontext, True, (20, 20, 20))
        self.buttonsurface.fill(self.normalColor)
        if self.buttonrect.collidepoint(self.mouse):
            self.buttonsurface.fill(self.hoverColor)
        elif self.is_clicked is True:
            self.buttonsurface.fill(self.retainedColor) 
        self.buttonsurface.blit(buttonsurf, [self.buttonrect.width/2 - buttonsurf.get_rect().width/2, 
                            self.buttonrect.height/2 - buttonsurf.get_rect().height/2])
        self.screen.blit(self.buttonsurface, self.buttonrect)
        pygame.draw.rect(self.screen, self.boundaryColor, self.buttonrect, 1)
    
    def animation(self):
        gamebutton.putbutton(self)
        i = self.i
        j = self.j
        if pygame.mouse.get_pressed(num_buttons=3)[0] and self.is_clicked is False:
            self.playerboard[i][j] = self.gameboard[i][j]
            self.is_clicked = True
            return self.playerboard
        # if right-clicked, flag the button with 'F
        elif pygame.mouse.get_pressed(num_buttons=3)[2] and self.is_clicked is False and self.is_flagged is False:
            self.playerboard[i][j] = 'F'
            self.is_flagged = True
            return self.playerboard
        elif pygame.mouse.get_pressed(num_buttons=3)[0] and self.is_clicked is True:
            print('already clicked')
            
class message_box():
    def __init__(self, width, height, x, y, screen):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.message_text = 'Starting'
        self.message_surface = pygame.Surface((self.width, self.height))
        self.screen = screen
        self.normalcolor = White
        self.is_loss = False
        self.is_win = False
        
    def put_message_box(self):
        self.message_surface.fill(self.normalcolor)
        message_text = self.message_text
        message_surf = font.render(message_text, True, (20, 20, 20))
        message_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.message_surface.blit(message_surf, [message_rect.width/2 - message_surf.get_rect().width/2, 
                message_rect.height/2 - message_surf.get_rect().height/2])
        self.screen.blit(self.message_surface, message_rect)
        pygame.draw.rect(self.screen, Black, message_rect, 1)