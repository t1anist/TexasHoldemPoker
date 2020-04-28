import random
from math import ceil


def hard_translate(real_act, pot):
    b = real_act / pot
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
    p_a = ((a/real_act)-(a/c)) / (1-(a/c))
    p_c = ((real_act/c)-(a/c)) / (1-(a/c))
    total = p_a + p_c
    choose = random.random()
    if choose <= (p_a / total):
        return abs_a
    else:
        return abs_c


def reverse_translate(abs_action, pot):
    a = 0
    if abs_action == 'f' or abs_action == 'c' or abs_action == 'a':
        return abs_action
    if abs_action == 'q':
        a = ceil(0.25 * pot)
    elif abs_action == 'h':
        a = ceil(0.5 * pot)
    elif abs_action == 'i':
        a = ceil(0.75 * pot)
    elif abs_action == 'p':
        a = pot
    elif abs_action == 'd':
        a = 2 * pot
    elif abs_action == 'v':
        a = 5 * pot
    elif abs_action == 't':
        a = 10 * pot
    b = 1 + random.random() * 0.3
    a = ceil(a*b)
    return a
