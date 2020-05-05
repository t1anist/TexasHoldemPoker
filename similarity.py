from poker_card import Property
from math import exp


bet_distance = {'q': 0, 'h': 1, 'i': 2, 'p': 3, 'd': 4, 'v': 5, 't': 6}
board_matrix = [[1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0.8, 0.7, 0, 0, 0, 0, 0],
                [0, 0.8, 1, 0.7, 0, 0, 0, 0, 0],
                [0, 0.7, 0.7, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0.8, 0.7, 0, 0.6],
                [0, 0, 0, 0, 0.8, 1, 0.7, 0, 0.5],
                [0, 0, 0, 0, 0.7, 0.7, 1, 0.8, 0.8],
                [0, 0, 0, 0, 0, 0, 0.8, 1, 0.8],
                [0, 0, 0, 0, 0.6, 0.5, 0.8, 0.8, 1]]


def cal_similarity(result):
    # hand_strength
    s1 = max((1 - (2 * abs(Property.hole_card_level - int(result[1])) / 45)), 0)
    # stack_commit
    s2 = exp(-(abs(Property.stack_commit - result[3])))
    # bet_sequence
    a = list(Property.bet_sequence)
    b = list(result[2])
    for i in a[::]:
        if i == '-':
            a.remove(i)
    for i in b[::]:
        if i == '-':
            b.remove(i)
    s3 = 0
    flag = 1
    if len(a) == len(b):
        c = a[::]
        d = b[::]
        for i in range(len(c)):
            if c[i] == 'a' or c[i] == 'c' or d[i] == 'a' or d[i] == 'c':
                if d[i] != c[i]:
                    flag = 0
                    break
                else:
                    b.remove(c[i])
                    a.remove(c[i])
        if flag:
            sum = 0
            if len(a) == 0 and len(b) == 0:
                s3 = 1
            else:
                for i in range(len(a)):
                    try:
                        sum += abs(bet_distance[a[i]] - bet_distance[b[i]])
                    except KeyError:
                        print(a)
                        print(b)
                s3 = 1 - 0.05 * sum
    else:
        s3 = 0
    # board_texture
    s4 = board_matrix[Property.board_texture.value][result[4]]
    # total
    return (s1+s2+s3+s4) / 4
