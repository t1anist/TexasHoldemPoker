import pygame
from pygame.sprite import Sprite
""" here is all the cards image definition"""
img2d = "cardimg/2d.png"; img2c =  "cardimg/2c.png";img2h =  "cardimg/2h.png";img2s =  "cardimg/2s.png"
img3d =  "cardimg/3d.png"; img3c =  "cardimg/3c.png";img3h =  "cardimg/3h.png";img3s =  "cardimg/3s.png"
img4d =  "cardimg/4d.png"; img4c =  "cardimg/4c.png";img4h =  "cardimg/4h.png";img4s =  "cardimg/4s.png"
img5d =  "cardimg/5d.png"; img5c =  "cardimg/5c.png";img5h =  "cardimg/5h.png";img5s =  "cardimg/5s.png"
img6d =  "cardimg/6d.png"; img6c =  "cardimg/6c.png";img6h =  "cardimg/6h.png";img6s =  "cardimg/6s.png"
img7d =  "cardimg/7d.png"; img7c =  "cardimg/7c.png";img7h =  "cardimg/7h.png";img7s =  "cardimg/7s.png"
img8d =  "cardimg/8d.png"; img8c =  "cardimg/8c.png";img8h =  "cardimg/8h.png";img8s =  "cardimg/8s.png"
img9d =  "cardimg/9d.png"; img9c =  "cardimg/9c.png";img9h =  "cardimg/9h.png";img9s =  "cardimg/9s.png"
img10d =  "cardimg/10d.png"; img10c =  "cardimg/10c.png";img10h =  "cardimg/10h.png";img10s =  "cardimg/10s.png"
imgJd =  "cardimg/Jd.png"; imgJc =  "cardimg/Jc.png";imgJh =  "cardimg/Jh.png";imgJs =  "cardimg/Js.png"
imgQd =  "cardimg/Qd.png"; imgQc =  "cardimg/Qc.png";imgQh =  "cardimg/Qh.png";imgQs =  "cardimg/Qs.png"
imgKd =  "cardimg/Kd.png"; imgKc =  "cardimg/Kc.png";imgKh =  "cardimg/Kh.png";imgKs =  "cardimg/Ks.png"
imgAd =  "cardimg/Ad.png"; imgAc =  "cardimg/Ac.png";imgAh =  "cardimg/Ah.png";imgAs =  "cardimg/As.png"
imgback =  "cardimg/back.png"; imgbackgray = "cardimg/backgray.png"
"""     image dictionary for indexing the correct file name of the images  """
img_Dict = {2: img2d, 22: img2c ,42: img2h, 62: img2s,3:img3d, 23:img3c, 43:img3h, 63:img3s, 4:img4d, 24:img4c, 44:img4h,  64:img4s, 5:img5d, 25:img5c, 45:img5h, 65:img5s,
           6:img6d, 26:img6c, 46:img6h, 66:img6s, 7:img7d, 27:img7c, 47:img7h, 67:img7s, 8:img8d, 28:img8c, 48:img8h, 68:img8s, 9:img9d, 29:img9c, 49:img9h, 69:img9s,
           10:img10d, 30:img10c, 50:img10h, 70:img10s, 11:imgJd, 31:imgJc, 51:imgJh, 71:imgJs, 12:imgQd, 32:imgQc, 52:imgQh, 72:imgQs, 13:imgKd,33:imgKc, 53:imgKh, 73:imgKs,
           14:imgAd, 34:imgAc, 54:imgAh, 74:imgAs }


# 卡片类，在屏幕中显示的位置
class Poker_card(Sprite):
    def __init__(self):
        super(Poker_card, self).__init__()
        # 初始化卡片并设置其初始位置
        self.image = pygame.image.load("cardimg/2d.png")
        self.rect = self.image.get_rect()


# 玩家类
class Player:
    num = 8  # 玩家人数
    ID = 1  # 本服务器游戏ID
    tempID = 1  # 临时ID
    time = 60  # 超时时间
    raise_money = 2  # 加注额
    up_money_flag = 0  # 增加加注按钮标志位
    down_money_flag = 0  # 减少加注按钮标志位
    up_down_num = 10  # 增减注的数量
    call_money = 2  # 跟注额
    state = 1  # 游戏状态
    pot_money = 0  # 池内筹码
    p_win = 0  # 牌力值
    hole_card_level = 0
    hand_card = [7, 8]
    public_card = [2, 3, 4, 5, 6]

    def __init__(self, num=2):
        self.name = 'xx'
        self.money = 1000   # 初始化金钱
        self.addr_list = [6, 6, 6, 6, 6]
        self.bet_money = 0


# 对手类
class Opponent():
    initial_money = 0
    bet_seq = ""
    bet_money = 0
    pot_money = 3


# 属性集
class Property:
    hole_card_level = 0
    bet_sequence = ""
    stack_commit = 0
    board_texture = 0
    action = ()
    outcome = ()

    @classmethod
    def printProperty(cls):
        print("hold_card_level:", cls.hole_card_level)
        print("bet_sequence:", cls.bet_sequence)
        print("stack_commit:", cls.stack_commit)
        print("board_texture", cls.board_texture)
