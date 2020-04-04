import pygame.font
from pygame.sprite import Sprite
class Textbox(Sprite):#文本框
    def __init__(self):
        super(Textbox,self).__init__()
#  显示文字使用的字体设置
        self.text_color = (30, 30, 30)#文字为黑色
        self.bg_color = (230,230,230)#背景为灰色
        self.font = pygame.font.SysFont('SimHei', 26)
#  准备初始文字图像
        """ 将文字转换为一幅渲染的图像 """
        msg = str('    ')
        self.image = self.font.render(msg, True, self.text_color,self.bg_color)
        self.rect = self.image.get_rect()
    def update_msg(self,msg):
        msg = str(msg)
        if msg == "跟注0":
            msg = "过牌"
        self.image = self.font.render(msg, True, self.text_color, self.bg_color)