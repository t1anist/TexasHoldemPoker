import socket
import threading
import re
import random
import time
from hole_cards_level import *
import action
from math import ceil
import boardTexture
import pymysql
from similarity import cal_similarity
clock_s = 0
clock_flag = 0
#牌组 （value,color)
deck = [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4), (5, 1), (5, 2),
        (5, 3), (5, 4), (6, 1), (6, 2), (6, 3), (6, 4), (7, 1), (7, 2), (7, 3), (7, 4), (8, 1), (8, 2), (8, 3), (8, 4),
        (9, 1), (9, 2), (9, 3), (9, 4), (10, 1), (10, 2), (10, 3), (10, 4), (11, 1), (11, 2), (11, 3), (11, 4), (12, 1),
        (12, 2), (12, 3), (12, 4), (13, 1), (13, 2), (13, 3), (13, 4), (14, 1), (14, 2), (14, 3), (14, 4)]
flag = 0

def get_card_power(num1, num2, num3, num4, num5, color1, color2, color3, color4, color5):  # 获得牌力一般方法
    """
    Determine the type of five cards
    :param num1: value of card 1
    :param num2: value of card 2
    :param num3: value of card 3
    :param num4: value of card 4
    :param num5: value of card 5
    :param color1: color of card 1
    :param color2: color of card 2
    :param color3: color of card 3
    :param color4: color of card 4
    :param color5: color of card 5
    :return: cards value of five cards
    """
    cards_list = [num1, num2, num3, num4, num5]  # 牌值 2-A 映射到 2 -14
    suites_list = [color1, color2, color3, color4, color5]  # 花色 映射到 1，2，3，4
    cards_list.sort()
    result = 0
    straight = 1
    for i in range(4):   # 顺子
        if cards_list[i] + 1 != cards_list[i + 1]:
            straight = 0
            break
    if len(set(suites_list)) == 1:  # 同花
        if straight == 1:
            result = cards_list[0]
            result = 9 << 20 | result  # 同花顺
        else:  # 同花
            for i in range(5):
                result = result | cards_list[i] << 4 * i
            result = 6 << 20 | result
    elif cards_list.count(cards_list[2]) == 4:  # 四条
        result = cards_list[1]
        result = 8 << 20 | result
    elif (cards_list.count(cards_list[0]) == 3 and cards_list.count(cards_list[4]) == 2) or \
            (cards_list.count(cards_list[0]) == 2 and cards_list.count(cards_list[4]) == 3):     # 葫芦
        result = cards_list[2]
        result = 7 << 20 | result
    elif cards_list == [2, 3, 4, 5, 14] or straight == 1:  # 顺子
        if cards_list[4] == 14:
            result = 1
        else:
            result = cards_list[0]
        result = 5 << 20 | result
    elif cards_list.count(cards_list[2]) == 3:  # 三条
        result = cards_list[2]
        result = 4 << 20 | result
    elif cards_list.count(cards_list[1]) == 2 and cards_list.count(cards_list[3]) == 2:  # 两对
        if cards_list.count(cards_list[0]) == 1:
            result = result | cards_list[3] << 8
            result = result | cards_list[1] << 4
            result = result | cards_list[0]
        elif cards_list.count(cards_list[2]) == 1:
            result = result | cards_list[3] << 8
            result = result | cards_list[1] << 4
            result = result | cards_list[2]
        elif cards_list.count(cards_list[4]) == 1:
            result = result | cards_list[3] << 8
            result = result | cards_list[1] << 4
            result = result | cards_list[4]
        result = 3 << 20 | result
    else:
        if cards_list[0] == cards_list[1]:  # 一对
            result = result | cards_list[0] << 12
            result = result | cards_list[4] << 8
            result = result | cards_list[3] << 4
            result = result | cards_list[2]
            result = 2 << 20 | result
        elif cards_list[1] == cards_list[2]:
            result = result | cards_list[1] << 12
            result = result | cards_list[4] << 8
            result = result | cards_list[3] << 4
            result = result | cards_list[0]
            result = 2 << 20 | result
        elif cards_list[2] == cards_list[3]:
            result = result | cards_list[2] << 12
            result = result | cards_list[4] << 8
            result = result | cards_list[1] << 4
            result = result | cards_list[0]
            result = 2 << 20 | result
        elif cards_list[3] == cards_list[4]:
            result = result | cards_list[3] << 12
            result = result | cards_list[2] << 8
            result = result | cards_list[1] << 4
            result = result | cards_list[0]
            result = 2 << 20 | result
        else:
            for i in range(5):
                result = result | cards_list[i] << 4 * i
            result = 1 << 20 | result
    return result

def rank(hand_card, public_card):
    """
    Return the maximum value of two hand cards and five public cards
    :param hand_card: two hand cards (value and color)
    :param public_card: five public cards (value and color)
    :return: maximum value of cards
    """
    max = 0
    poker_card = [hand_card[0], hand_card[1], public_card[0], public_card[1], public_card[2], public_card[3],
                  public_card[4]]
    for a in range(3):
        for b in range(a + 1, 4):
            for c in range(b + 1, 5):
                for d in range(c + 1, 6):
                    for e in range(d + 1, 7):
                        temp = get_card_power(poker_card[a][0], poker_card[b][0], poker_card[c][0], poker_card[d][0],
                                              poker_card[e][0], poker_card[a][1], poker_card[b][1], poker_card[c][1],
                                              poker_card[d][1], poker_card[e][1])
                        if max < temp:
                            max = temp
    return max


def get_p_win(hand1, hand2, public_card1=0, public_card2=0, public_card3=0, public_card4=0, public_card5=0):
    cnt = 0
    temp = deck.copy()
    try:
        temp.remove(hand1)
        temp.remove(hand2)
    except ValueError:
        pass
    hand = [hand1, hand2]
    if public_card3 != 0 and public_card4 == 0:
        temp.remove(public_card1)
        temp.remove(public_card2)
        temp.remove(public_card3)
    if public_card4 != 0 and public_card5 == 0:
        temp.remove(public_card4)
    if public_card5 != 0:
        temp.remove(public_card5)
    for i in range(100):
        random.shuffle(temp)  # 洗牌
        hand_card = [temp[0], temp[1]]
        if public_card3 == 0:
            public_card = [temp[2], temp[3], temp[4], temp[5], temp[6]]
        elif public_card4 == 0:
            public_card = [public_card1, public_card2, public_card3, temp[2], temp[3]]
        elif public_card5 == 0:
            public_card = [public_card1, public_card2, public_card3, public_card4, temp[2]]
        else:
            public_card = [public_card1, public_card2, public_card3, public_card4, public_card5]
        if rank(hand, public_card) > rank(hand_card, public_card):
            cnt += 1
    Player.p_win = int(cnt / 1)
    msg_p_win.update_msg("绝对牌力值:" + str(Player.p_win))
    msg_p_win.rect = msg_p_win.image.get_rect()
    msg_p_win.rect.centerx = center_x3
    msg_p_win.rect.bottom = screen_height
    msgs.add(msg_p_win)
    return Player.p_win


def action_AI():
    global db
    time.sleep(2)
    Property.hole_card_level = Player.hole_card_level
    Property.bet_sequence = Opponent.bet_seq
    Property.stack_commit = ceil((Opponent.initial_money - player[2].money) / (Opponent.initial_money / 4))
    Property.board_texture = boardTexture.getBoardTexture()
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='woshi250ma?', db='poker', charset='utf8')
    cursor = db.cursor()
    sql = "select * from result"
    cursor.execute(sql)
    results = cursor.fetchall()
    similarity = 0
    sameone = tuple()
    for result in results:
        temp_simi = cal_similarity(result)
        if similarity < temp_simi:
            similarity = temp_simi
            sameone = result
    # print(sameone)
    action = str(sameone[5]).split(',')
    choice = random.random()
    sum = 0.0
    for i in range(len(action)):
        temp_str = "%.9f" % (float(action[i]))
        sum += float(temp_str)
        # print("Choice is" + str(choice) + ' temp_str is ' + temp_str + 'sum is ' + str(sum))
        if choice <= sum:
            # print(i)
            send(i)
            break
    # time.sleep(2)
    # if p_win<20:  # 胜率低于20 就直接弃牌
    #     tcp_socket.send("弃牌".encode( 'gbk'))
    # elif p_win<40: # 胜率低于40 根据跟注大小进行弃牌或者跟注操作
    #     if Player.call_money > p_win*p_win/70:
    #         tcp_socket.send("弃牌".encode('gbk'))
    #     else:
    #         tcp_socket.send(("跟注，" + str(Player.call_money)).encode('gbk'))
    # else:
    #     if int(6 * p_win * p_win / 1000) <= Player.call_money:
    #         if p_win<60:
    #             tcp_socket.send("弃牌".encode('gbk'))
    #         else:
    #             tcp_socket.send(("跟注，" + str(Player.call_money)).encode('gbk'))
    #     else:
    #         tcp_socket.send(("加注，" + str(int(6*p_win*p_win/1000))).encode('gbk'))


def send(num):
    if num == 0:
        tcp_socket.send("弃牌".encode('gbk'))
    elif num == 1:
        call = Player.call_money
        if player[1].money < Player.call_money:
            call = player[1].money
        tcp_socket.send(("跟注，" + str(call)).encode('gbk'))
    elif num == 2:
        call = action.reverse_translate('q', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 3:
        call = action.reverse_translate('h', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 4:
        call = action.reverse_translate('i', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 5:
        call = action.reverse_translate('p', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 6:
        call = action.reverse_translate('d', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 7:
        call = action.reverse_translate('v', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 8:
        call = action.reverse_translate('t', Opponent.pot_money) + Player.call_money
        if player[1].money < call:
            call = player[1].money
        tcp_socket.send(("加注，" + str(call)).encode('gbk'))
    elif num == 9:
        tcp_socket.send(("加注，" + str(player[1].money)).encode('gbk'))


def f_t(num):
    num = int(num)
    suit = int(num / 20)
    return (num - suit * 20, suit + 1)


def game_Init():
    Player.state = 0
    game_resulet_msg.kill()  # 清除每局的结果
    for i in range(0, 8):
        msg_action[i + 1].kill()  # 清除选手上局的动作
    Player.pot_money = 0  # 底池清零
    Opponent.bet_seq = ''
    Opponent.bet_money = 0
    show_cards(player)  # 显示纸牌
    pos = play_pos_Dict[Player.num]  # 根据玩家人数确定每个玩家的位置
    for i in pos:
        create_card(player[0], 0, i, 2)
        create_card(player[0], 1, i, 2)
    msgs.add(clock_msg)


def up_money():  # 更新每人的筹码数
    if Player.ID == 1:
        s = "每人筹码："
        for i in range(Player.num):
            s += "$" + str(player[i+1].money)
        tcp_socket.send(s.encode('gbk'))


def login(data,tcp_socket):
    global flag
    ret = re.match(r"登录成功！剩余筹码数为：([0-9]*)", data)
    if ret:
        flag = 1
        print("等待他人进入游戏中···")
        return
    if data == "用户密码错误，请重新输入" or data == "注册成功，请重新登录" or data == "请输入正确的账户和密码" or data == "该用户已登录！请换个用户试试":
        name = input("请输入你的用户名：")
        password = input("请输入你的密码：")
        s = '用户名：' + str(name) + "密码：" + str(password)
        tcp_socket.send(s.encode('gbk'))
    ret = re.match(r"不存在该用户，是否注册该用户yes/no?", data)
    if ret:
        ans = input()
        tcp_socket.send(ans.encode('gbk'))


def game_ready(data):
    ret = re.match(r".*你的ID：([1-8])", data)
    if ret:
        Player.ID = int(ret.group(1))  # 获取自己的ID
    ret = re.match(r".*玩家名字：(.*)", data)
    if ret:
        temp = re.findall(r"\@(.*?)\@", ret[1])  # 名字
        Player.num = len(temp)
        for i in range(Player.num):
            print(temp[i])
            player[i + 1].name = temp[i]
        temp = re.findall(r"\$([0-9|\-]*)", ret[1])  # 筹码
        for i in range(Player.num):
            player[i + 1].money = int(temp[i])
        Opponent.initial_money = player[2].money
        pos = play_pos_Dict[Player.num]
        for i in pos:
            create_card(player[0], 0, i, 2)
            create_card(player[0], 1, i, 2)
        for i in range(1, Player.num + 1):
            pos_dict[i] = pos[(i + Player.num - Player.ID) % Player.num]
            update_msg_money(i, 0)
        show_player_name()


# tcp客户端程序
# 接收到的信息分为公有信息和私有信息，公有信息所有玩家都可以看到，私有信息仅自己可见
def recv_msg(tcp_socket):
    global clock_flag,flag
    flag = 0
    # name = input("请输入你的用户名：")
    # password = input("请输入你的密码：")
    # TODO : ban the login
    # s = '用户名：' + str(name) + "密码：" + str(password)
    s = '用户名：AI密码：123'
    tcp_socket.send(s.encode('gbk'))
    while 1:
        data = tcp_socket.recv(1024)
        data = data.decode("gbk")
        print(data)
        if data == "其他玩家已退出，请重新连接":
            print("收到退出指令,请玩家重启程序")
            pygame.quit()
            return
        if flag == 0:  # 登录注册
            login(data, tcp_socket)
        while flag == 1:  # 进入游戏等待
            pass
        if flag >= 2:  # 游戏中
            game_ready(data)
            ret = re.match(r".*开始游戏.*", data)
            if ret:
                game_Init()
                flag = 2
            ret = re.match(r".*玩家([1-8])为庄", data)
            if ret:
                banker.update(pos_dict[int(ret.group(1))])
            ret = re.findall(r"玩家([1-8])的手牌是：([0-9]{1,2})，([0-9]{1,2})", data)
            if ret:
                for i in range(len(ret)):
                    num1 = int(ret[i][0])
                    num2 = int(ret[i][1])
                    num3 = int(ret[i][2])
                    update_cards(player, num1, num2, num3)
                    if Player.ID == num1 and len(ret) == 1 and flag == 2:
                        Player.hand_card = [f_t(num2), f_t(num3)]
                        Player.hole_card_level = get_hole_card_level(Player.hand_card[0], Player.hand_card[1])
                        get_p_win(Player.hand_card[0], Player.hand_card[1])
            ret = re.match(r".*玩家([1-8])下小盲注：([0-9]{1,4})，玩家([1-8])下大盲注：([0-9]{1,4})", data)
            if ret:
                update_msg_action(int(ret[1]), "小盲注" + str(ret[2]))
                update_msg_action(int(ret[3]), "大盲注" + str(ret[4]))
                update_msg_money(int(ret[1]), int(ret[2]))
                update_msg_money(int(ret[3]), int(ret[4]))
                if int(ret[1]) != Player.ID:
                    Opponent.bet_money = int(ret[2])
                elif int(ret[2]) != Player.ID:
                    Opponent.bet_money = int(ret[4])
                player[int(ret[1])].bet_money = int(ret[2])
                player[int(ret[3])].bet_money = int(ret[4])
                Player.raise_money = Player.call_money = int(ret[4])
                msg_bet_money.update_msg(Player.call_money)
                msgs.add(msg_bet_money)
            ret = re.match(r".*前三张公共牌为：([0-9]{1,2})[，]([0-9]{1,2})[，]([0-9]{1,2})", data)
            if ret:
                for i in range(1, 9):
                    player[i].bet_money = 0
                update_cards(player, 0, int(ret.group(1)), int(ret.group(2)), int(ret.group(3)))
                Player.public_card[0] = f_t(ret.group(1))
                Player.public_card[1] = f_t(ret.group(2))
                Player.public_card[2] = f_t(ret.group(3))
                get_p_win(Player.hand_card[0], Player.hand_card[1],Player.public_card[0],Player.public_card[1],Player.public_card[2])
                Opponent.bet_seq += '-'
                Opponent.pot_money = Player.pot_money
            ret = re.match(r".*第四张公共牌为：([0-9]{1,2})", data)
            if ret:
                for i in range(1, 8):
                    player[i].bet_money = 0
                player[0].addr_list[3] = int(ret.group(1))
                create_card(player[0], 3, 0)
                Player.public_card[3] = f_t(ret.group(1))
                get_p_win(Player.hand_card[0], Player.hand_card[1], Player.public_card[0], Player.public_card[1],
                          Player.public_card[2],Player.public_card[3])
                Opponent.bet_seq += '-'
                Opponent.pot_money = Player.pot_money
            ret = re.match(r".*第五张公共牌为：([0-9]{1,2})", data)
            if ret:
                for i in range(1, 8):
                    player[i].bet_money = 0
                player[0].addr_list[4] = int(ret.group(1))
                create_card(player[0], 4, 0)
                Player.public_card[4] = f_t(ret.group(1))
                get_p_win(Player.hand_card[0], Player.hand_card[1], Player.public_card[0], Player.public_card[1],
                          Player.public_card[2], Player.public_card[3], Player.public_card[4])
                Opponent.bet_seq += '-'
                Opponent.pot_money = Player.pot_money
                flag = 3
            ret = re.match(r".*玩家([1-8])的动作为：(弃牌)", data)
            if ret:
                update_msg_action(int(ret.group(1)), ret.group(2))
                if ret[1] == '2':
                    Opponent.bet_seq += 'f'
            ret = re.match(r".*玩家([1-8])的动作为：(跟注|加注)，([0-9]*)", data)
            if ret:
                update_msg_action(int(ret.group(1)), ret.group(2) + ret.group(3))
                update_msg_money(int(ret.group(1)), int(ret.group(3)) - player[int(ret.group(1))].bet_money)
                player[int(ret.group(1))].bet_money = int(ret.group(3))
                if ret[1] == '2':
                    if ret[2] == u"跟注":
                        Opponent.bet_seq += 'c'
                    elif ret[2] == u"加注":
                        if player[2].money == 0:
                            Opponent.bet_seq += 'a'
                        else:
                            Opponent.bet_seq += action.soft_translate(int(ret[3]), Opponent.pot_money)
                    Opponent.bet_money = int(ret.group(3))
            ret = re.match(r".*玩家([1-8])行动中，([0-9]*)", data)
            if ret:
                update_msg_action(int(ret.group(1)), " ")
                Player.call_money = Player.raise_money = int(ret.group(2))
                msg_bet_money.update_msg(Player.call_money)
                clock_flag = 1
                player_clock.update(pos_dict[int(ret.group(1))])  # 倒计时
                clock_msg.update_msg(str(Player.time))
                clock_msg.rect = clock_msg.image.get_rect()
                clock_msg.rect.centerx = player_clock.rect.centerx
                clock_msg.rect.centery = player_clock.rect.centery
                Player.tempID = int(ret.group(1))
                if Player.ID == int(ret.group(1)):  # 轮到自己行动了
                    ret = re.match(r"AI", player[Player.ID].name)
                    if ret:
                        action_AI()
                    else:
                        buttons.add(pass_button)
                        if Player.call_money == 0:
                            call_button.update_msg("过牌")
                        else:
                            call_button.update_msg("跟注")
                        buttons.add(call_button)
                        buttons.add(Raise_button)
                        buttons.add(bet_money_raise)
                        buttons.add(bet_money_down)
            ret = re.match(r".*玩家([1-8])获得胜利！(.*)", data)
            if ret:
                update_msg_money(int(ret.group(1)), -Player.pot_money)
                show_result(int(ret.group(1)), ret.group(2))
                clock_msg.kill()
                Opponent.bet_seq = ''
                Opponent.pot_money = 3
                Player.state = 1
                buttons.add(play_button)
                up_money()
                Opponent.initial_money = player[2].money
                Player.public_card = [2, 3, 4, 5, 6]
            ret = re.match(r".*玩家([1-8])和玩家([1-8])平局！(.*)", data)
            if ret:
                update_msg_money(int(ret.group(1)), -Player.pot_money / 2, 1)
                update_msg_money(int(ret.group(2)), -Player.pot_money / 2, 1)
                show_result(int(ret.group(1)), ret.group(3), 1)
                clock_msg.kill()
                Opponent.bet_seq = ''
                Opponent.pot_money = 3
                Player.state = 1
                buttons.add(play_button)
                up_money()
                Opponent.initial_money = player[2].money
                Player.public_card = [2, 3, 4, 5, 6]
            ret = re.match(r".*玩家([1-8])玩家([1-8])玩家([1-8])平局！(.*)", data)
            if ret:
                update_msg_money(int(ret.group(1)), -Player.pot_money / 3, 1)
                update_msg_money(int(ret.group(2)), -Player.pot_money / 3, 1)
                update_msg_money(int(ret.group(3)), -Player.pot_money / 3, 1)
                show_result(int(ret.group(1)), ret.group(4), 1)
                clock_msg.kill()
                Opponent.bet_seq = ''
                Opponent.pot_money = 3
                Player.state = 1
                buttons.add(play_button)
                up_money()
                Opponent.initial_money = player[2].money
                Player.public_card = [2, 3, 4, 5, 6]
            if play_button in buttons:
                ret = re.match(r"AI", player[Player.ID].name)
                if ret:
                    if Player.state == 1:
                        play_button.kill()
                        time.sleep(3)
                        tcp_socket.send(("准备好了".encode('gbk')))
                        Player.state = 2

# 1s 的定时中断函数
def clock_start():
    global clock_s, clock_flag
    if clock_flag == 1:
        clock_flag = 0
        clock_s = 0
    elif Player.state == 0:
        clock_s += 1
    clock_msg.update_msg(str(Player.time - clock_s))
    clock_msg.rect = clock_msg.image.get_rect()
    clock_msg.rect.centerx = player_clock.rect.centerx
    clock_msg.rect.centery = player_clock.rect.centery
    timer = threading.Timer(1, clock_start)
    timer.setDaemon(True)  # 设置守护线程
    timer.start()
    if Player.ID == Player.tempID and clock_s == Player.time and Player.state == 0:  # 规定时间没做出操作则自动弃牌:
        action_pass(tcp_socket)


feature = ['ip']
if __name__ == "__main__":
    filename = 'ip.txt'
    #  读取文件操作
    dect = {}
    with open(filename) as file_object:
        for line in file_object:
            s = line.rstrip()
            print(s)
            ret = re.match(r'(.*):(.*)', s)
            if ret:
                dect[ret.group(1)] = ret.group(2)   # 增加键值对
    # 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("正在连接ip：", dect['ip'])
    port = 6677
    while True:
        try:
            print("尝试进入房间", port)
            tcp_socket.connect((dect['ip'], port))  # 设定好ip和端口后才能正常运行程序  192.168.124.13
        except TimeoutError:
            ip = input("ip设置错误，请重新输入ip：")
            dect['ip'] = ip
            with open(filename, 'w') as file_object:
                for i in range(len(feature)):
                    file_object.write(feature[i]+":")
                    file_object.write(dect[feature[i]]+'\n')
        except ConnectionRefusedError:
            print("服务器未打开，请联系服务人X员！")
        else:
            data = tcp_socket.recv(1024)
            data = data.decode("gbk")
            if data == "连接成功！":
                print("连接成功！")
                break
            port += 1
            tcp_socket.close()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p = threading.Thread(target=recv_msg, args=(tcp_socket,))
    p.setDaemon(True)  # 设置守护线程
    p.start()  # 创建线程
    while flag == 0:
        pass
    from game_functions import *
    show_cards(player)  # 显示纸牌
    buttons.add(play_button)
    flag = 2
    clock_start()
    while 1:
        check_events(tcp_socket)  # 鼠标键盘响应
        update_screen(screen, cards, buttons, msgs)  # 屏幕更新
