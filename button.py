import pygame


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
        # self.hov_1 = self._create_image(color_hover, outline, gameboard[x][y], text_color, tmp_rect)
        self.org_2 = self._create_image(pressed_color, outline, 'F', (255, 50, 50), tmp_rect)
        self.hov_2 = self._create_image(color_hover, outline, 'F', (255, 50, 50), tmp_rect)
        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        # init x, y, playerboard, gameboard
    
    def _create_image(self, color, outline, text, text_color, rect):
        img = pygame.Surface(rect.size)
        font = pygame.font.SysFont("Arial", 20)
        if outline:
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
                else:
                # check which button was clicked
                # 1 == left mouse button, 3 == right mouse button
                    self.right_clicked = True
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


