import sys
from settings import *
from pygame.sprite import Group
from pygame.locals import *
from poker_card import *
from textbox import Textbox
from clock import Clock
from banker import Banker
from button import Button
def check_events(tcp_socket):
    # 响应按键和鼠标
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 退出
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 按键响应
            if event.key == pygame.K_q:  # q键退出
                sys.exit()
            elif event.key == pygame.K_w:  # w键全屏
                screen = pygame.display.set_mode((1300, 680), FULLSCREEN, 32)  # 全屏
            elif event.key == pygame.K_e:  # e键退出全屏
                screen = pygame.display.set_mode((1300, 680))  # 屏幕大小
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标响应
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_button.rect.collidepoint(mouse_x, mouse_y):  # 开始游戏
                if Player.state == 1:
                    if player[Player.ID].money > 5:
                        Player.state = 0
                        play_button.kill()
                        tcp_socket.send(("准备好了".encode('gbk')))
                    else:
                        print("玩家筹码不足，不能进行游戏")
            if bet_money_raise.rect.collidepoint(mouse_x, mouse_y):  # 加注
                Player.up_money_flag = 1
                Player.raise_money += 1
                msg_bet_money.update_msg(Player.raise_money)
            elif bet_money_down.rect.collidepoint(mouse_x, mouse_y):  # 减注
                Player.down_money_flag = 1
                Player.raise_money -= 1
                Player.raise_money = max(Player.raise_money, 0)
                msg_bet_money.update_msg(Player.raise_money)
            if Player.tempID == Player.ID:
                if pass_button.rect.collidepoint(mouse_x, mouse_y):  # 玩家要弃牌
                    action_pass(tcp_socket)
                elif call_button.rect.collidepoint(mouse_x, mouse_y):  # 玩家要跟注
                    action_call(tcp_socket)
                elif Raise_button.rect.collidepoint(mouse_x, mouse_y):  # 玩家要加注
                    if Player.raise_money > Player.call_money:
                        action_raise(tcp_socket)
        elif event.type == pygame.MOUSEBUTTONUP:  #鼠标弹起
            Player.up_money_flag = 0
            Player.down_money_flag = 0
            Player.up_down_num = 3
    if Player.up_money_flag != 0:
        Player.up_money_flag += 1
        if  Player.up_money_flag > Player.up_down_num:
            Player.up_down_num = Player.up_down_num - 1
            Player.up_money_flag = 1
            Player.raise_money += 1
            msg_bet_money.update_msg(Player.raise_money)
    if  Player.down_money_flag != 0:
        Player.down_money_flag += 1
        if Player.down_money_flag > Player.up_down_num:
            Player.up_down_num = Player.up_down_num - 1
            Player.down_money_flag = 1
            Player.raise_money -= 1
            Player.raise_money = max(Player.raise_money,0)
            msg_bet_money.update_msg(Player.raise_money)


def kill_buttons():
    Player.tempID = 0
    pass_button.kill()
    call_button.kill()
    Raise_button.kill()
    bet_money_raise.kill()
    bet_money_down.kill()


def action_pass(tcp_socket):
    kill_buttons()
    tcp_socket.send("弃牌".encode('gbk'))


def action_call(tcp_socket):
    kill_buttons()
    if player[Player.ID].money >= Player.call_money:
        tcp_socket.send(("跟注，" + str(Player.call_money)).encode('gbk'))
    else:
        tcp_socket.send("弃牌".encode('gbk'))


def action_raise(tcp_socket):
    kill_buttons()
    if player[Player.ID].money >= Player.raise_money:
        tcp_socket.send(("加注，" + str(Player.raise_money)).encode('gbk'))
    elif player[Player.ID].money >= Player.call_money:
        tcp_socket.send(("跟注，" + str(Player.call_money)).encode('gbk'))
    else:
        tcp_socket.send("弃牌".encode('gbk'))


# 刷新屏幕
def update_screen(screen, cards, buttons, msgs):
    screen.fill((230, 230, 230))  # 填充背景
    if clock_msg in msgs:
        player_clock.blitme(screen)   # 秒表
        banker.blitme(screen)  # 庄家标志
    cards.draw(screen)  # 显示卡片
    buttons.draw(screen)  # 显示按钮
    msgs.draw(screen)  # 显示信息
    pygame.display.flip()  # 显示信息


# 创造一张卡片
def create_card(player, num, pos, is_show=1):
    card = Poker_card()  # 实例化一张卡片
    if pos == 0:       # 公共牌摆放位置
        card.rect.centerx = screen_rect.centerx + (num - 2) * card.rect.width
        card.rect.centery = screen_rect.centery
    elif pos == 1:  # 手牌位置1
        card.rect.centerx = center_x1 + (num * 2 - 1) * card.rect.width/2
        card.rect.bottom = bottom_y1
    elif pos == 2:  # 手牌位置2
        card.rect.centerx = center_x2 + (num * 2 - 1) * card.rect.width / 2
        card.rect.bottom = bottom_y2
    elif pos == 3:  # 手牌位置3
        card.rect.centerx = center_x3 + (num * 2 - 1) * card.rect.width / 2
        card.rect.centery = center_y3
    elif pos == 4:  # 手牌位置4
        card.rect.centerx = center_x4 + (num * 2 - 1) * card.rect.width / 2
        card.rect.top = top_y4
    elif pos == 5:  # 手牌位置5
        card.rect.centerx = center_x5 + (num * 2 - 1) * card.rect.width / 2
        card.rect.top = top_y5
    elif pos == 6:  # 手牌位置6
        card.rect.centerx = center_x6 + (num * 2 - 1) * card.rect.width / 2
        card.rect.top = top_y6
    elif pos == 7:  # 手牌位置7
        card.rect.centerx = center_x7 + (num * 2 - 1) * card.rect.width / 2
        card.rect.centery = center_y7
    elif pos == 8:  # 手牌位置8
        card.rect.centerx = center_x8 + (num * 2 - 1) * card.rect.width / 2
        card.rect.bottom = bottom_y8
    # 重新设置显示的卡片
    if is_show == 0:
        if pos == 0:
            card.image = pygame.image.load("cardimg/back.png")
        else:
            card.image = pygame.image.load("cardimg/backgray.png")
    elif is_show == 1:
        card.image = pygame.image.load(img_Dict[player.addr_list[num]])
    else:
        card.image = pygame.image.load("cardimg/back.png")
    cards.add(card)


# 按钮位置初始化   开始游戏，弃牌，跟注，加注，加减注
def button_init():
    play_button.rect.left = screen_rect.centerx + 290
    play_button.rect.centery = screen_rect.centery - 50
    pass_button.rect.centerx = screen_rect.centerx - 140
    pass_button.rect.bottom = call_button.rect.bottom = Raise_button.rect.bottom = bottom_y1 - card_height-60
    call_button.rect.centerx = screen_rect.centerx
    Raise_button.rect.centerx = screen_rect.centerx + 140
    bet_money_raise.rect.centerx = screen_rect.centerx + 150
    bet_money_raise.rect.bottom = screen_rect.bottom - 140
    bet_money_down.rect.centerx = screen_rect.centerx + 150
    bet_money_down.rect.bottom = screen_rect.bottom - 60
    # buttons.add(play_button)


# 文本框初始化
def create_msgs():
    clock_msg.rect.centerx = player_clock.rect.centerx
    clock_msg.rect.centery = player_clock.rect.centery
    clock_msg.font = pygame.font.SysFont('SimHei', 22)
    clock_msg.update_msg(str(90))
    clock_msg.rect = clock_msg.image.get_rect()
    msg_bet_money.rect.centerx = screen_rect.centerx + 150
    msg_bet_money.rect.bottom = screen_rect.bottom - 100


# 显示玩家num的动作
def update_msg_action(player_id, action):
    if pos_dict[player_id] == 1:
        msg_action[1].rect.left = center_x1 - card_width
        msg_action[1].rect.bottom = bottom_y1 - card_height
        msg_action[1].update_msg(action)
        msgs.add(msg_action[1])
    elif pos_dict[player_id] == 2:
        msg_action[2].rect.left = center_x2 - card_width
        msg_action[2].rect.bottom = bottom_y2 - card_height
        msg_action[2].update_msg(action)
        msgs.add(msg_action[2])
    elif pos_dict[player_id] == 3:
        msg_action[3].rect.left = center_x3 - card_width
        msg_action[3].rect.bottom = center_y3 - card_height/2
        msg_action[3].update_msg(action)
        msgs.add(msg_action[3])
    elif pos_dict[player_id] == 4:
        msg_action[4].rect.left = center_x4 - card_width
        msg_action[4].rect.top = top_y4 + card_height
        msg_action[4].update_msg(action)
        msgs.add(msg_action[4])
    elif pos_dict[player_id] == 5:
        msg_action[5].rect.left = center_x5 - card_width
        msg_action[5].rect.top = top_y5 + card_height
        msg_action[5].update_msg(action)
        msgs.add(msg_action[5])
    elif pos_dict[player_id] == 6:
        msg_action[6].rect.left = center_x6 - card_width
        msg_action[6].rect.top = top_y6 + card_height
        msg_action[6].update_msg(action)
        msgs.add(msg_action[6])
    elif pos_dict[player_id] == 7:
        msg_action[7].rect.left = center_x7
        msg_action[7].rect.bottom = center_y7 - card_height/2
        msg_action[7].update_msg(action)
        msgs.add(msg_action[7])
    elif pos_dict[player_id] == 8:
        msg_action[8].rect.left = center_x8 - card_width
        msg_action[8].rect.bottom = bottom_y8 - card_height
        msg_action[8].update_msg(action)
        msgs.add(msg_action[8])


# 显示玩家num的本金
def update_msg_money(player_id, money, flag = 0):
    player[player_id].money -= int(money)
    if flag == 0:
        Player.pot_money += int(money)
    msg_pot_money.update_msg("Pot:"+str(Player.pot_money))
    msg_pot_money.rect = msg_pot_money.image.get_rect()
    msg_pot_money.rect.centerx = screen_rect.centerx
    msg_pot_money.rect.bottom = screen_rect.centery - card_height/2
    msgs.add(msg_pot_money)

    if pos_dict[player_id] == 1:
        msg_money[1].rect.left = center_x1 + 5
        msg_money[1].rect.bottom = screen_height
        msg_money[1].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[1])
    if pos_dict[player_id] == 2:
        msg_money[2].rect.left = center_x2 + 5
        msg_money[2].rect.bottom = screen_height
        msg_money[2].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[2])
    if pos_dict[player_id] == 3:
        msg_money[3].rect.left = center_x3 + 5
        msg_money[3].rect.top = center_y3 + card_height/2
        msg_money[3].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[3])
    if pos_dict[player_id] == 4:
        msg_money[4].rect.left = center_x4 + 5
        msg_money[4].rect.top = 0
        msg_money[4].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[4])
    if pos_dict[player_id] == 5:
        msg_money[5].rect.left = center_x5 + 5
        msg_money[5].rect.top = 0
        msg_money[5].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[5])
    if pos_dict[player_id] == 6:
        msg_money[6].rect.left = center_x6 + 5
        msg_money[6].rect.top = 0
        msg_money[6].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[6])
    if pos_dict[player_id] == 7:
        msg_money[7].rect.left = center_x7 + 5
        msg_money[7].rect.top = center_y7 + card_height/2
        msg_money[7].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[7])
    if pos_dict[player_id] == 8:
        msg_money[8].rect.left = center_x8 + 5
        msg_money[8].rect.bottom = screen_height
        msg_money[8].update_msg("筹码"+str(player[player_id].money))
        msgs.add(msg_money[8])

# 显示玩家名字
def show_player_name():
    for i in range(1, Player.num + 1):
        if pos_dict[i] == 1:
            msg_name[1].rect.left = center_x1 - card_width
            msg_name[1].rect.bottom = screen_height
            msg_name[1].update_msg(player[i].name)
            msgs.add(msg_name[1])
        elif pos_dict[i] == 2:
            msg_name[2].rect.left = center_x2 - card_width
            msg_name[2].rect.bottom = screen_height
            msg_name[2].update_msg(player[i].name)
            msgs.add(msg_name[2])
        elif pos_dict[i] == 3:
            msg_name[3].rect.left = center_x3 - card_width
            msg_name[3].rect.top = center_y3 + card_height/2
            msg_name[3].update_msg(player[i].name)
            msgs.add(msg_name[3])
        elif pos_dict[i] == 4:
            msg_name[4].rect.left = center_x4 - card_width
            msg_name[4].rect.top = 0
            msg_name[4].update_msg(player[i].name)
            msgs.add(msg_name[4])
        elif pos_dict[i] == 5:
            msg_name[5].rect.left = center_x5 - card_width
            msg_name[5].rect.top = 0
            msg_name[5].update_msg(player[i].name)
            msgs.add(msg_name[5])
        elif pos_dict[i] == 6:
            msg_name[6].rect.left = center_x6 - card_width
            msg_name[6].rect.top = 0
            msg_name[6].update_msg(player[i].name)
            msgs.add(msg_name[6])
        elif pos_dict[i] == 7:
            msg_name[7].rect.left = center_x7 - card_width
            msg_name[7].rect.top = center_y7 + card_height/2
            msg_name[7].update_msg(player[i].name)
            msgs.add(msg_name[7])
        elif pos_dict[i] == 8:
            msg_name[8].rect.left = center_x8 - card_width
            msg_name[8].rect.bottom = screen_height
            msg_name[8].update_msg(player[i].name)
            msgs.add(msg_name[8])


def show_cards(player):
    pos  = play_pos_Dict[Player.num]
    for i in range(Player.num + 1):
        if i == 0:
            create_card(player[i], 0, i, 0)  # 显示5张公共牌
            create_card(player[i], 1, i, 0)
            create_card(player[i], 2, i, 0)
            create_card(player[i], 3, i, 0)
            create_card(player[i], 4, i, 0)
        else:
            create_card(player[(i + Player.ID - 1)%(Player.num+1)], 0, pos[i-1], 0)  #显示2张手牌
            create_card(player[(i + Player.ID - 1)%(Player.num+1)], 1, pos[i-1], 0)

#显示游戏结果
def show_result(winner_ID, rank, flag = 0):
    if flag == 0:
        game_resulet_msg.update_msg(player[winner_ID].name + "获得胜利!" + rank)
    else:
        game_resulet_msg.update_msg("平局！！！" + rank)
    game_resulet_msg.rect = game_resulet_msg.image.get_rect()
    game_resulet_msg.rect.centerx = screen_rect.centerx
    game_resulet_msg.rect.bottom = screen_rect.centery - card_height/2
    msgs.add(game_resulet_msg)

#  显示玩家num 的手牌
def update_cards(player, num, card_num1, card_num2, card_num3 = 0):
    player[num].addr_list[0] = card_num1
    player[num].addr_list[1] = card_num2
    if num == 0:
        player[num].addr_list[2] = card_num3
        create_card(player[0], 0, 0)
        create_card(player[0], 1, 0)
        create_card(player[0], 2, 0)
    else:
        pos = play_pos_Dict[Player.num]
        create_card(player[num], 0, pos[(num + Player.num - Player.ID) % Player.num])
        create_card(player[num], 1, pos[(num + Player.num - Player.ID) % Player.num])



# 初始化游戏并创建一个屏幕对象

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))  # 屏幕大小
screen_rect = screen.get_rect()  # 获取屏幕矩形
pygame.display.set_caption("德州扑克多人对战游戏")  # 标题
#  按钮
play_button = Button("Start Game")  # 开始游戏按键
restart_button = Button("Restart")  # 重新开始游戏按键
bet_money_raise = Button(" + ")
bet_money_down = Button(" - ")
pass_button = Button("弃 牌")  # 弃牌
call_button = Button("跟 注")  # 跟注
Raise_button = Button("加 注")  # 加注
player_clock = Clock()  # 倒计时秒表
banker = Banker()  # 庄家按钮
#  文本框
game_resulet_msg = Textbox()  # 游戏结果显示
clock_msg = Textbox()  # 倒计时秒表

player = []
player0 = Player(5)  # 公共牌
player.append(player0)
for i in range(8):
    player.append(Player())  # 生成8个玩家

msg_name = [' ']       # 名字信息
for i in range(8):
     msg_name.append(Textbox())  # 生成8个名字信息

msg_money = [' ']      # 金钱信息
for i in range(8):
    msg_money.append(Textbox())   # 生成8个金钱信息

msg_action = [' ']   # 玩家动作信息
for i in range(8):
    msg_action.append(Textbox())  # 生成8个玩家的动作信息

msg_bet_money = Textbox() # 赌注
msg_pot_money = Textbox()  # 钱池
msg_p_win = Textbox()  # 获奖概率

cards = Group()  # 创建一个存储卡片的编组
buttons = Group()  # 创建一个按键的编组
msgs = Group()  # 创建一个信息的编组
button_init()
create_msgs()

db = ''