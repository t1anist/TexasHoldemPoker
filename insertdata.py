import pymysql
import re
from hole_cards_level import get_hole_card_level
from math import ceil
from boardTexture import boardTexture
from collections import Counter


# 对手集
class Opponent:
    bet_money = 0
    pot_money = 0
    ai_bet = 0


# 属性集
class Property:
    hole_card_level = 0
    bet_sequence = ""
    stack_commit = 0
    board_texture = 0
    action = ''
    outcome = 0
    hand_id = 0

    def __init__(self, hand_id=0, hole_card_level=0, bet_sequence='', stack_commit=0, board_texture=0, action='', outcome=0):
        self.hand_id = hand_id
        self.hole_card_level = hole_card_level
        self.bet_sequence = bet_sequence
        self.stack_commit = stack_commit
        self.board_texture = board_texture
        self.action = action
        self.outcome = outcome


def translate(bet_moeny, pot):
    b = bet_moeny / pot
    a = 0
    c = 0
    abs_a = ''
    abs_c = ''
    if b <= 0.25:
        return 'q'
    elif 0.25 < b < 0.5:
        a, c = 0.25, 0.5
        abs_a, abs_c = 'q', 'h'
    elif b == 0.5:
        return 'h'
    elif 0.5 < b < 0.75:
        a, c = 0.5, 0.75
        abs_a, abs_c = 'h', 'i'
    elif b == 0.75:
        return 'i'
    elif 0.75 < b < 1:
        a, c = 0.75, 1
        abs_a, abs_c = 'i', 'p'
    elif b == 1:
        return 'p'
    elif 1 < b < 2:
        a, c = 1, 2
        abs_a, abs_c = 'p', 'd'
    elif b == 2:
        return 'd'
    elif 2 < b < 5:
        a, c = 2, 5
        abs_a, abs_c = 'd', 'v'
    elif b == 5:
        return 'v'
    elif 5 < b < 10:
        a, c = 5, 10
        abs_a, abs_c = 'v', 't'
    elif b >= 10:
        return 't'
    a *= pot
    c *= pot
    if (a / bet_moeny) > (bet_moeny / c):
        return abs_a
    else:
        return abs_c


def getBoardTexture():
    card_list = []
    suit_list = []
    flush = 0
    straight = 0
    if len(public_card) == 5:
        card_list = [public_card[0][0], public_card[1][0], public_card[2][0],
                     public_card[3][0], public_card[4][0]]
        card_list.sort()
        suit_list = [public_card[0][1], public_card[1][1], public_card[2][1],
                     public_card[3][1], public_card[4][1]]
        straight = find_straight(card_list)
        flush = find_flush(card_list)
        if straight > 2:
            if flush < 3:
                return boardTexture.No_Salient
            elif flush == 3:
                return boardTexture.Flush_Possible
            elif flush > 3:
                return boardTexture.Flush_High_Possible
        elif straight == 2:
            if flush < 3:
                return boardTexture.Straight_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_Possible
            elif flush > 3:
                return boardTexture.Flush_High_Possible_Straight_Possible
        elif straight < 2:
            if flush < 3:
                return boardTexture.Straight_High_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_High_Possible
            elif flush > 3:
                return boardTexture.Flush_High_Possible_Straight_High_Possible
    elif len(public_card) == 4:
        card_list = [public_card[0][0], public_card[1][0], public_card[2][0],
                     public_card[3][0]]
        card_list.sort()
        suit_list = [public_card[0][1], public_card[1][1], public_card[2][1],
                     public_card[3][1]]
        straight = find_straight(card_list)
        flush = find_flush(card_list)
        if straight > 2:
            if flush < 3:
                return boardTexture.No_Salient
            elif flush == 3:
                return boardTexture.Flush_Possible
            elif flush > 3:
                return boardTexture.Flush_High_Possible
        elif straight == 2:
            if flush < 3:
                return boardTexture.Straight_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_Possible
            elif flush > 3:
                return boardTexture.Flush_High_Possible_Straight_Possible
        elif straight < 2:
            if flush < 3:
                return boardTexture.Straight_High_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_High_Possible
            elif flush > 3:
                return boardTexture.Flush_High_Possible_Straight_High_Possible
    elif len(public_card) == 3:
        card_list = [public_card[0][0], public_card[1][0], public_card[2][0]]
        card_list.sort()
        suit_list = [public_card[0][1], public_card[1][1], public_card[2][1]]
        straight = find_straight(card_list)
        flush = find_flush(card_list)
        if straight > 2:
            if flush < 3:
                return boardTexture.No_Salient
            elif flush == 3:
                return boardTexture.Flush_Possible
        elif straight == 2:
            if flush < 3:
                return boardTexture.Straight_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_Possible
    else:
        return boardTexture.No_Salient


def find_straight(card_list):
    temp_list = card_list.copy()
    if len(card_list) == 5:
        # 差0张
        if all_straight(card_list) or card_list == [2, 3, 4, 5, 14]:
            return 0
        # 差1张 / 两张
        for i in range(5):
            temp_list = card_list.copy()
            temp_list.remove(temp_list[i])
            straight = find_straight(temp_list)
            if straight < 3:
                return straight
        return 3
    elif len(card_list) == 4:
        # 差1张
        # 1或5号位
        if all_straight(card_list) or card_list == [3, 4, 5, 14]:
            return 1
        # 2号位
        temp_list = card_list.copy()
        temp_list[0] += 1
        if all_straight(temp_list) or temp_list == [3, 4, 5, 14]:
            return 1
        # 3号位
        temp_list = card_list.copy()
        temp_list[0] += 1
        temp_list[1] += 1
        if all_straight(temp_list) or temp_list == [3, 4, 5, 14]:
            return 1
        # 4号位
        temp_list = card_list.copy()
        temp_list[3] -= 1
        if all_straight(temp_list) or temp_list == [2, 3, 4, 13]:
            return 1
        # 差两张
        for i in range(4):
            temp_list = card_list.copy()
            temp_list.remove(temp_list[i])
            if find_straight(temp_list) == 2:
                return 2
        return 3
    elif len(card_list) == 3:
        # 差两张
        # 012 123 234
        if all_straight(card_list) or card_list == [4, 5, 14]:
            return 2
        # 013
        temp_list = [card_list[0], card_list[1], card_list[2]-1]
        if all_straight(temp_list):
            return 2
        # 014
        temp_list = [card_list[0], card_list[1], card_list[2]-2]
        if all_straight(temp_list) or temp_list == [2, 3, 12]:
            return 2
        # 023
        temp_list = [card_list[0]+1, card_list[1], card_list[2]]
        if all_straight(temp_list):
            return 2
        # 024
        temp_list = [card_list[0]+1, card_list[1], card_list[2]-1]
        if all_straight(temp_list) or temp_list == [3, 4, 13]:
            return 2
        # 034
        temp_list = [card_list[0]+2, card_list[1], card_list[2]]
        if all_straight(temp_list) or temp_list == [4, 5, 14]:
            return 2
        # 124
        temp_list = [card_list[0], card_list[1], card_list[2]-1]
        if all_straight(temp_list) or temp_list == [3, 4, 13]:
            return 2
        # 134
        temp_list = [card_list[0]+1, card_list[1], card_list[2]]
        if all_straight(temp_list) or temp_list == [4, 5, 14]:
            return 2
        return 3


def all_straight(card_list):
    flag = True
    for i in range(len(card_list)-1):
        if card_list[i + 1] != card_list[i] + 1:
            flag = False
            break
    return flag


def find_flush(card_list):
    c = Counter(card_list)
    max = 0
    for i in c.values():
        if i > max:
            max = i
    return max


public_card = []
items = []
suit = {'d': 1, 'h': 2, 's': 3, 'c': 4}
num = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='woshi250ma?', db='poker', charset='utf8')
    cursor = db.cursor()
    with open(
            r"D:\毕业设计\德州扑克\德州扑克数据\DeepStack_vs_IFP_pros\DeepStack_logs\PokerStars\DeepStack_view\all_hands.bachmann"
            r".juergen.log", 'r') as fp:
        lines = fp.readlines()
    # with open(r"D:\Tian\Desktop\temp.txt", 'r') as fp:
    #     lines = fp.readlines()
    initial_money = 20000
    for line in lines:
        # 处理空白行
        if line == '\n':
            for item in items:
                if not item.bet_sequence and not item.action:
                    continue
                item.outcome = Property.outcome
                sql = 'INSERT INTO test(hand_id, hole_card_level, bet_sequence, stack_commit, board_texture, action, outcome) \
                        values(%d,%d,\'%s\',%d,%d,\'%s\',%d)' % (item.hand_id, item.hole_card_level, item.bet_sequence,
                                                                 item.stack_commit, item.board_texture, item.action,
                                                                 item.outcome)
                print(sql)
                cursor.execute(sql)
            Property.hand_id = 0
            Property.hole_card_level = 0
            Property.bet_sequence = ''
            Property.stack_commit = 0
            Property.board_texture = 0
            Property.action = ''
            Property.outcome = 0
            Opponent.bet_money = 0
            Opponent.pot_money = 0
            Opponent.ai_bet = 0
            initial_money = 20000
            items.clear()
            public_card.clear()
        # 处理非空白行
        line = line.strip('\n')
        # 处理开始行
        ret = re.match(r"^PokerStars Hand #([0-9]+)", line)
        if ret:
            Property.hand_id = int(ret[1])
            print(line)
            continue
        # 处理盲注行
        ret = re.match(r"([a-zA-Z.]+): posts (small|big) blind \$(\d+)", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                if ret[2] == 'small':
                    Opponent.bet_money = 50
                    Opponent.ai_bet = 100
                elif ret[2] == 'big':
                    Opponent.bet_money = 100
                    Opponent.ai_bet = 50
                Opponent.pot_money += 150
            continue
        # 处理手牌行
        ret = re.match(r"Dealt to DeepStack \[([0-9TJQKA]{1,2})([a-z]) ([0-9TJQKA]{1,2})([a-z])]", line)
        if ret:
            Property.hole_card_level = get_hole_card_level((num[ret[1]], suit[ret[2]]), (num[ret[3]], suit[ret[4]]))
            Property.stack_commit = ceil(Opponent.bet_money / (initial_money / 4))
            continue
        # 处理行为行
        # 弃牌
        ret = re.match(r"([a-zA-Z.]+): folds", line)
        if ret:
            if ret[1] == 'DeepStack':
                Property.action = 'f'
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
            continue
        # call all-in
        ret = re.match(r"([a-zA-Z.]+): calls \$([0-9]+) and is all-in", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += 'a'
                Opponent.bet_money += int(ret[2])
                Opponent.pot_money += int(ret[2])
                Property.stack_commit = 4
                continue
            elif ret[1] == 'DeepStack':
                Opponent.ai_bet += int(ret[2])
                Opponent.pot_money += int(ret[2])
                Property.action = 'a'
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # call
        ret = re.match(r"([a-zA-Z.]+): calls \$([0-9]+)", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += 'c'
                Opponent.bet_money += int(ret[2])
                Opponent.pot_money += int(ret[2])
                Property.stack_commit = ceil(Opponent.bet_money / (initial_money / 4))
                continue
            elif ret[1] == 'DeepStack':
                Property.action = 'c'
                Opponent.ai_bet += int(ret[2])
                Opponent.pot_money += int(ret[2])
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # raise all-in
        ret = re.match(r"([a-zA-Z.]+): raises \$([0-9]+) to \$([0-9]+) and is all-in", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += 'a'
                Opponent.bet_money += abs(Opponent.ai_bet - Opponent.bet_money) + int(ret[2])
                Opponent.pot_money += abs(Opponent.ai_bet - Opponent.bet_money) + int(ret[2])
                Property.stack_commit = ceil(Opponent.bet_money / (initial_money / 4))
                continue
            elif ret[1] == 'DeepStack':
                Property.action = 'a'
                Opponent.ai_bet += abs(Opponent.bet_money - Opponent.ai_bet) + int(ret[2])
                Opponent.pot_money += abs(Opponent.bet_money - Opponent.ai_bet) + int(ret[2])
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # raise
        ret = re.match(r"([a-zA-Z.]+): raises \$([0-9]+) to \$([0-9]+)", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += translate(int(ret[2]), Opponent.pot_money)
                Opponent.bet_money += abs(Opponent.ai_bet - Opponent.bet_money) + int(ret[2])
                Opponent.pot_money += abs(Opponent.ai_bet - Opponent.bet_money) + int(ret[2])
                Property.stack_commit = ceil(Opponent.bet_money / (initial_money / 4))
                continue
            elif ret[1] == 'DeepStack':
                Property.action = translate(int(ret[2]), Opponent.pot_money)
                Opponent.ai_bet += abs(Opponent.bet_money - Opponent.ai_bet) + int(ret[2])
                Opponent.pot_money += abs(Opponent.bet_money - Opponent.ai_bet) + int(ret[2])
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # bet all-in
        ret = re.match(r"([a-zA-Z.]+): bets \$([0-9]+) and is all-in", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += 'a'
                Opponent.bet_money += int(ret[2])
                Opponent.pot_money += int(ret[2])
                Property.stack_commit = ceil(Opponent.bet_money / (initial_money / 4))
                continue
            elif ret[1] == 'DeepStack':
                Property.action = 'a'
                Opponent.ai_bet += int(ret[2])
                Opponent.pot_money += int(ret[2])
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # bet
        ret = re.match(r"([a-zA-Z.]+): bets \$([0-9]+)", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += translate(int(ret[2]), Opponent.pot_money)
                Opponent.bet_money += int(ret[2])
                Opponent.pot_money += int(ret[2])
                Property.stack_commit = ceil(Opponent.bet_money / (initial_money / 4))
                continue
            elif ret[1] == 'DeepStack':
                Property.action = translate(int(ret[2]), Opponent.pot_money)
                Opponent.ai_bet += int(ret[2])
                Opponent.pot_money += int(ret[2])
                items.append(
                    Property(Property.hand_id, Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # check
        ret = re.match(r"([a-zA-Z.]+): checks", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.bet_sequence += 'c'
                continue
            elif ret[1] == 'DeepStack':
                Property.action = 'c'
                items.append(
                    Property(Property.hand_id,Property.hole_card_level, Property.bet_sequence, Property.stack_commit,
                             Property.board_texture, Property.action))
                continue
        # FLOP
        ret = re.match(r"\*\*\* FLOP \*\*\*\* \[([0-9TJQKA]{1,2})([a-z]) ([0-9TJQKA]{1,2})([a-z]) ([0-9TJQKA]{1,2})([a-z])]", line)
        if ret:
            public_card = [(num[ret[1]], suit[ret[2]]), (num[ret[3]], suit[ret[4]]), (num[ret[5]], suit[ret[6]])]
            Property.board_texture = getBoardTexture().value
            Property.bet_sequence += '-'
            continue
        # TURN
        ret = re.match(r"\*\*\* TURN \*\*\*\* \[([0-9TJQKA]{1,2})([a-z])]", line)
        if ret:
            public_card.append((num[ret[1]], suit[ret[2]]))
            Property.board_texture = getBoardTexture().value
            Property.bet_sequence += '-'
            continue
        # River
        ret = re.match(r"\*\*\* RIVER \*\*\*\* \[([0-9TJQKA]{1,2})([a-z])]", line)
        if ret:
            public_card.append((num[ret[1]], suit[ret[2]]))
            Property.board_texture = getBoardTexture().value
            Property.bet_sequence += '-'
            continue
        # 匹配收益
        ret = re.match(r"([a-zA-Z.]+) collected \$([0-9]+) from (the )*pot", line)
        if ret:
            if ret[1] == 'bachmann.juergen':
                Property.outcome = -ceil(0.5 * int(ret[2]))
                continue
            elif ret[1] == 'DeepStack':
                Property.outcome = ceil(0.5 * int(ret[2]))
                continue
        print(line)
    db.commit()
    cursor.close()
    db.close()
