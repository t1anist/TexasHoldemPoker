from poker_card import Property
from math import exp


bet_distance = {'q':0, 'h':1, 'i':2, 'p':3, 'd':4, 'v':5, 't':6}


def cal_similarity(result):
    # hand_strength
    s1 = max(1 - (2 * abs(Property.hole_card_level - result[1]) / 45))
    # stack_commit
    s2 = exp(-(abs(Property.stack_commit - result[3])))
    # bet_sequence
    a = list(Property.bet_sequence)
    b = list(result[2])
    for i in a[::]:
        if i == '-':
            a.remove(i)
    for i in b[::]:
        if b == '-':
            b.remove(i)
    s3 = 0
    flag = 1
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] == 'a' or a[i] == 'c':
                if b[i] != a[i]:
                    flag = 0
        if flag:
            sum = 0
            for i in range(len(a)):
                sum += abs(bet_distance[a[i]] - bet_distance[b[i]])
            s3 = 1 - 0.05 * sum
    # board_texture
    # TODO : finish board texture similarity

