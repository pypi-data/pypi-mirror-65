import pygame
from pygame.locals import *

def getRect(surf, align, x, y):
    if align == 'center':
        return surf.get_rect(center=(x,y))
    elif align == 'topleft':
        return surf.get_rect(topleft=(x,y))


class TextBox(object):
    def __init__(self, x, y, text = '', color = (0,0,0), fontSize = 60, fontFamily = None, align ='center', screen=None):
        super().__init__()       
        self.align = align
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font(fontFamily, fontSize)
        self.setText(text)
        self.screen = screen


    def setText(self, text):
        self.text_surf = self.font.render(text, True, self.color)
        self.rect = getRect(self.text_surf, self.align,self.x, self.y)

    

    def draw(self, screen=None):
        if screen is not None:
            self.screen = screen
        self.screen.blit(self.text_surf, self.rect)

    def setPosition(self, x, y):
        self.rect = getRect(self.text_surf, self.align,x,y)

class Button:
    def __init__(self, x, y, w, h, color = (102,102,102), activeColor = (150,150,150), text = '', textColor = (255,255,255), fontSize = 30, fontFamily = None, align='center', screen=None):
        super().__init__()
        self.surf = pygame.Surface((w,h))
        self.surf.fill(color)
        self.rect = getRect(self.surf, align, x, y)
        self.color = color
        self.activeColor = activeColor
        self.textColor = textColor
        self.align = align
        self.font = pygame.font.Font(fontFamily, fontSize)
        self.x = x
        self.y = y
        self.screen = screen
        self.setText(text)
        
        

    def draw(self,screen=None):
        if screen is not None:
            self.screen = screen

        self.screen.blit(self.surf, self.rect)   
        self.screen.blit(self.text_surf, self.text_rect) 
    
    def setText(self, text):
        self.text = text
        self.text_surf = self.font.render(self.text, True, self.textColor)
        self.text_rect = getRect(self.text_surf, self.align, self.x, self.y)
        self.rect.center = self.text_rect.center

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.setText(self.text)

    

    def isPressed(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                return True
            self.surf.fill(self.activeColor)
        else:
            self.surf.fill(self.color)
        return False