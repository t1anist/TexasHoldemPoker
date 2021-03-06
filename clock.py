import pygame
from settings import *
class Clock():  # 闹钟
    def __init__(self):
        self.image = pygame.image.load('img/clock.png')
        self.rect = self.image.get_rect()
        self.update(1)
    def update(self,pos):
        if pos == 1:
            self.rect.centerx = center_x1
            self.rect.centery = bottom_y1 - card_height - self.rect.height/2
        elif pos == 2:
            self.rect.centerx = center_x2
            self.rect.centery = bottom_y2 - card_height - self.rect.height/2
        elif pos == 3:
            self.rect.centerx = center_x3 - card_width - self.rect.width / 2
            self.rect.centery = center_y3
        elif pos == 4:
                self.rect.centerx = center_x4
                self.rect.centery = top_y4 + card_height + self.rect.height/2
        elif pos == 5:
                self.rect.centerx = center_x5
                self.rect.centery = top_y5 + card_height + self.rect.height/2
        elif pos == 6:
                self.rect.centerx = center_x6
                self.rect.centery = top_y6 + card_height + self.rect.height/2
        elif pos == 7:
                self.rect.centerx = center_x7 + card_width + self.rect.width/2
                self.rect.centery = center_y7
        elif pos == 8:
            self.rect.centerx = center_x8
            self.rect.centery = bottom_y8 - card_height - self.rect.height/2
        if pos !=3 and pos != 7:
            self.rect.centerx = self.rect.centerx + 30
    def blitme(self,screen):
        #在制定位置绘制闹钟
        screen.blit(self.image,self.rect)