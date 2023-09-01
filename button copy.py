#Reference: https://stackoverflow.com/questions/57557599/why-wont-my-button-change-color-when-i-hover-over-it-pygame 
import pygame

pygame.init()

display_width = 1200
display_height = 600

# use python style variable names (lowercase)
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Log In')
clock = pygame.time.Clock()

# load the font only once instead of every frame
font = pygame.font.SysFont('arial', 20)

playerboard = [[0,2],[2,3]]
gameboard = [['X', 5],['F','F']]

# Class game button is a button class specifically for the gameboard
# if user left-clicks, it will reveal the number underneath
# if user right-clicks, it will flag the button
class game_button(pygame.sprite.Sprite):
    def __init__(self, color, color_hover, pressed_color, text_color, rect, x, y, 
                 playerboard, gameboard, outline = None):
        super().__init__()
        # init x, y, playerboard, gameboard
        self.x = x
        self.y = y
        self._playerboard = playerboard
        self._gameboard = gameboard
        # a temporary Rect to store the size of the button
        tmp_rect = pygame.Rect(0, 0, *rect.size)
        self.clicked = False
        self.right_clicked = False
        # create two Surfaces here, one the normal state, and one for the hovering state
        # we create the Surfaces here once, so we can simple blit them and dont have
        # to render the text and outline again every frame
        self.org = self._create_image(color, outline, playerboard[x][y], text_color, tmp_rect)
        self.hov = self._create_image(color_hover, outline, playerboard[x][y], text_color, tmp_rect)
        self.org_1 = self._create_image(pressed_color, outline, gameboard[x][y], text_color, tmp_rect)
        self.hov_1 = self._create_image(color_hover, outline, gameboard[x][y], text_color, tmp_rect)
        self.org_2 = self._create_image(color, outline, 'F', text_color, tmp_rect)
        self.hov_2 = self._create_image(color_hover, outline, 'F', text_color, tmp_rect)
        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        # init x, y, playerboard, gameboard
    
    def _create_image(self, color, outline, text, text_color, rect):
        img = pygame.Surface(rect.size)
        if outline:
            # here we can make good use of Rect's functions again
            # first, fill the Surface in the outline color
            # then fill a rectangular area in the actual color
            # 'inflate' is used to 'shrink' the rect
            img.fill(outline)
            img.fill(color, rect.inflate(-2, -2))
        else:
            img.fill(color)
        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(str(text), 1, text_color)
            # again, see how easy it is to center stuff using Rect's attributes like 'center'
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        return img

    def update(self, events):
        # here we handle all the logic of the Button
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        # if the mouse in inside the Rect (again, see how the Rect class
        # does all the calculation for use), use the 'hov' image instead of 'org'
        for event in events:
            # the Button checks for events itself.
            # if this Button is clicked, it runs the callback function
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                if event.button == 1:
                    self.clicked = True
                    self.update_board(self._playerboard, self._gameboard, self.x, self.y)
                    print(self._playerboard)
                else:
                # check which button was clicked
                # 1 == left mouse button, 3 == right mouse button
                    self.right_clicked = True
                    print(self._playerboard)
                # if the button is clicked, the callback function will be called
        # if left-clicked, the Button will change its color, and change the text to text_1
        # if right-clicked, the Button will change its color, and change the text to 'F'
        if self.clicked == True:
            self.image = self.org_1
        elif self.right_clicked == True:
            self.image = self.hov_2 if hit else self.org_2
        else:
            self.image = self.hov if hit else self.org
      
    @staticmethod        
    def update_board(playerboard, gameboard, x, y):
        playerboard[x][y] = gameboard[x][y]

class Button(pygame.sprite.Sprite):
    # 1) no need to have 4 parameters for position and size, use pygame.Rect instead
    # 2) let the Button itself handle which color it is
    # 3) give a callback function to the button so it can handle the click itself 
    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.text = text
        # a temporary Rect to store the size of the button
        tmp_rect = pygame.Rect(0, 0, *rect.size)
        # create two Surfaces here, one the normal state, and one for the hovering state
        # we create the Surfaces here once, so we can simple blit them and dont have
        # to render the text and outline again every frame
        self.org = self._create_image(color, outline, text, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, tmp_rect)
        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        self.callback = callback

    def _create_image(self, color, outline, text, rect):
        # function to create the actual surface
        # see how we can make use of Rect's virtual attributes like 'size'
        img = pygame.Surface(rect.size)
        if outline:
            # here we can make good use of Rect's functions again
            # first, fill the Surface in the outline color
            # then fill a rectangular area in the actual color
            # 'inflate' is used to 'shrink' the rect
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -4))
        else:
            img.fill(color)

        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(text, 1, pygame.Color('black'))
            # again, see how easy it is to center stuff using Rect's attributes like 'center'
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        return img

    def update(self, events):
        # here we handle all the logic of the Button
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        # if the mouse in inside the Rect (again, see how the Rect class
        # does all the calculation for use), use the 'hov' image instead of 'org'
        self.image = self.hov if hit else self.org
        for event in events:
            # the Button checks for events itself.
            # if this Button is clicked, it runs the callback function
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)


class general_button(pygame.sprite.Sprite):
    def __init__(self, color, color_hover, text_color, rect, callback = print('clicked'), 
                 text = '', text_1 = '', retained_clicked = False, outline=None):
        super().__init__()
        tmp_rect = pygame.Rect(0, 0, *rect.size)
        self.retained_clicked = retained_clicked
        self.clicked = False
        self.org = self._create_image(color, outline, text, text_color, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, text_color, tmp_rect)
        if retained_clicked == True:
            self.org_1 = self._create_image(color_hover, outline, text_1, text_color, tmp_rect)
        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        self.callback = callback

    def _create_image(self, color, outline, text, text_color, rect):
        # function to create the actual surface
        # see how we can make use of Rect's virtual attributes like 'size'
        font = pygame.font.SysFont("Arial", 20)
        img = pygame.Surface(rect.size)
        if outline:
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -4))
        else:
            img.fill(color)
        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(text, 1, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        return img

    def update(self, events):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                if self.retained_clicked:
                    self.callback
                    self.clicked = True
                else:
                    self.callback
        if self.clicked:
            self.image = self.org_1
        else:
            self.image = self.hov if hit else self.org
    
    # @staticmethod
    # def clicked_function():
    #     return print('Clicked!')


run = True
# we store all Sprites in a Group, so we can easily
# call the 'update' and 'draw' functions of the Buttons
# in the main loop
sprites = pygame.sprite.Group()
sprites.add(game_button(pygame.Color('green'), 
                   pygame.Color('red'), 
                   pygame.Color('blue'), pygame.Color('white'),
                   pygame.Rect(150, 200, 90, 100),0,0, playerboard, gameboard))

sprites.add(Button(pygame.Color('dodgerblue'), 
                   pygame.Color('lightgreen'), 
                   pygame.Rect(300, 200, 90, 100), 
                   lambda b: print(f"Click me again!"),
                   'Another'))

sprites.add(general_button(pygame.Color('red'),pygame.Color('green'), pygame.Color('white'), pygame.Rect(450, 200, 90, 100), 
                           text= 'Another', text_1= 'Anothered', retained_clicked= True))

while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # update all sprites
    # it now doesn't matter if we have one or 200 Buttons
    sprites.update(events)
    # clear the screen
    screen.fill(pygame.Color('white'))
    # draw all sprites/Buttons
    sprites.draw(screen)
    pygame.display.update()
    
    # limit framerate to 60 FPS
    clock.tick(60)