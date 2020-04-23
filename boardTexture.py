from enum import Enum
from poker_card import Player

class boardTexture(Enum):
    No_Salient = 0
    Flush_Possible = 1
    Straight_Possible = 2
    Flush_Possible_Straight_Possible = 3
    Straight_High_Possible = 4
    Flush_Possible_Straight_High_Possible = 5
    Flush_High_Possible = 6
    Flush_High_Possible_Straight_Possible = 7
    Flush_High_Possible_Straight_High_Possible = 8


def getBoardTexture():
    card_list = []
    suit_list = []
    flush = 0
    straight = 0
    if isinstance(Player.public_card[4], tuple):
        card_list = [Player.public_card[0][0], Player.public_card[1][0], Player.public_card[2][0],
                     Player.public_card[3][0], Player.public_card[4][0]]
        card_list.sort()
        suit_list = [Player.public_card[0][1], Player.public_card[1][1], Player.public_card[2][1],
                     Player.public_card[3][1], Player.public_card[4][1]]
        straight = find_straight(card_list)
        flush = len(set(suit_list))
        if straight > 2:
            if flush > 3:
                return boardTexture.No_Salient
            elif flush == 3:
                return boardTexture.Flush_Possible
            elif flush <= 2:
                return boardTexture.Flush_High_Possible
        elif straight == 2:
            if flush > 3:
                return boardTexture.Straight_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_Possible
            elif flush <= 2:
                return boardTexture.Flush_High_Possible_Straight_Possible
        elif straight < 2:
            if flush > 3:
                return boardTexture.Straight_High_Possible
            elif flush == 3:
                return boardTexture.Flush_Possible_Straight_High_Possible
            elif flush <= 2:
                return boardTexture.Flush_High_Possible_Straight_High_Possible
    elif isinstance(Player.public_card[3], tuple):
        card_list = [Player.public_card[0][0], Player.public_card[1][0], Player.public_card[2][0],
                     Player.public_card[3][0]]
        card_list.sort()
        suit_list = [Player.public_card[0][1], Player.public_card[1][1], Player.public_card[2][1],
                     Player.public_card[3][1]]
        straight = find_straight(card_list)
        flush = len(set(suit_list))
        if straight > 2:
            if flush > 2:
                return boardTexture.No_Salient
            elif flush == 2:
                return boardTexture.Flush_Possible
            elif flush == 2:
                return boardTexture.Flush_High_Possible
        elif straight == 2:
            if flush > 2:
                return boardTexture.Straight_Possible
            elif flush == 2:
                return boardTexture.Flush_Possible_Straight_Possible
            elif flush == 1:
                return boardTexture.Flush_High_Possible_Straight_Possible
        elif straight < 2:
            if flush > 2:
                return boardTexture.Straight_High_Possible
            elif flush == 2:
                return boardTexture.Flush_Possible_Straight_High_Possible
            elif flush == 1:
                return boardTexture.Flush_High_Possible_Straight_High_Possible
    elif isinstance(Player.public_card[2], tuple):
        card_list = [Player.public_card[0][0], Player.public_card[1][0], Player.public_card[2][0]]
        card_list.sort()
        suit_list = [Player.public_card[0][1], Player.public_card[1][1], Player.public_card[2][1]]
        straight = find_straight(card_list)
        flush = len(set(suit_list))
        if straight > 2:
            if flush > 1:
                return boardTexture.No_Salient
            elif flush == 1:
                return boardTexture.Flush_Possible
        elif straight == 2:
            if flush > 1:
                return boardTexture.Straight_Possible
            elif flush == 1:
                return boardTexture.Flush_Possible_Straight_Possible
    else:
        return boardTexture.No_Salient


def find_straight(card_list):
    temp_list = card_list.copy()
    if len(card_list) == 5:
        # 差0张
        if card_list == [2, 3, 4, 5, 14]:
            return 0
        if all_straight(card_list):
            return 0
        # 差1张
        for i in range(4):
            temp_list[i] = card_list[i+1]-1
            if all_straight(temp_list):
                return 1
            if i <= 2 and temp_list == [2, 3, 4, 5, 14]:
                return 1
            temp_list = card_list.copy()
        temp_list[4] = card_list[3] + 1
        if all_straight(temp_list):
            return 1
        temp_list = card_list.copy()
        temp_list[4] = 14
        if temp_list == [2, 3, 4, 5, 14]:
            return 1
        # 差2张
        temp_list = card_list.copy()
        # 12号位
        if temp_list[2:] == [4, 5, 14] or all_straight(temp_list[2:]):
            return 2
        # 13号位
        temp_list = card_list.copy()
        temp_list[0] = temp_list[1]-1
        temp_list[2] = temp_list[1]+1
        if all_straight(temp_list) or temp_list == [2, 3, 4, 5, 14]:
            return 2
        # 14号位
        temp_list = card_list.copy()
        temp_list[0] = temp_list[1]-1
        temp_list[3] = temp_list[2]+1
        if all_straight(temp_list) or temp_list == [2, 3, 4, 5, 14]:
            return 2
        # 15号位
        temp_list = card_list.copy()
        temp_list[0] = temp_list[1]-1
        temp_list[4] = temp_list[3]+1
        if all_straight(temp_list):
            return 2
        # 23号位
        temp_list = card_list.copy()
        temp_list[1] = temp_list[0]+1
        temp_list[2] = temp_list[1]+1
        if all_straight(temp_list) or temp_list == [2, 3, 4, 5, 14]:
            return 2
        # 24号位
        temp_list = card_list.copy()
        temp_list[1] = temp_list[0]+1
        temp_list[3] = temp_list[2]+1
        if all_straight(temp_list) or temp_list == [2, 3, 4, 5, 14]:
            return 2
        # 25号位
        temp_list = card_list.copy()
        temp_list[1] = temp_list[0]+1
        temp_list[4] = temp_list[3]+1
        if all_straight(temp_list):
            return 2
        # 34号位
        temp_list = card_list.copy()
        temp_list[2] = temp_list[1]+1
        temp_list[3] = temp_list[2]+1
        if all_straight(temp_list) or temp_list == [2, 3, 4, 5, 14]:
            return 2
        # 35号位
        temp_list = card_list.copy()
        temp_list[2] = temp_list[3]-1
        temp_list[4] = temp_list[3]+1
        if all_straight(temp_list):
            return 2
        # 45号位
        temp_list = card_list.copy()
        temp_list[3] = temp_list[2]+1
        temp_list[4] = temp_list[3]+1
        if all_straight(temp_list):
            return 2
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
