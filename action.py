import random


def hard_translate(real_act, pot):
    b = real_act / pot
    a = 0
    c = 0
    abs_a = ''
    abs_c = ''
    if b == 0.25:
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
    elif b == 10:
        return 't'
    else:
        return 'a'
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
