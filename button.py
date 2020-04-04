import pygame.font
from pygame.sprite import Sprite
class Button(Sprite):#按键
    state = 0    #全局状态
    def __init__(self,msg):
        super(Button,self).__init__()
        self.button_color = (0, 100, 0)   #绿色  按钮背景颜色
        self.text_color = (255, 255, 255) #白色 文字颜色
        self.font = pygame.font.SysFont('SimHei', 36)#字体及大小
        #  创建按钮的 rect 对象，并使其居中
        """ 将 msg 渲染为图像，并使其在按钮上居中 """
        self.image = self.font.render(msg, True, self.text_color,
                                            self.button_color)
        self.rect = self.image.get_rect()
    def update_msg(self,msg):
        msg = str(msg)
        self.image = self.font.render(msg, True, self.text_color, self.button_color)