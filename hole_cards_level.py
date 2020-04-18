import re
level = {1: [r"14,[1-4],14,[1-4]"],
         2: [r"13,[1-4],13,[1-4]"],
         3: [r"12,[1-4],12,[1-4]"],
         4: [r"11,[1-4],11,[1-4]"],
         5: [r"13,([1-4]),14,\1"],
         6: [r"12,([1-4]),14,\1"],
         7: [r"10,[1-4],10,[1-4]"],
         8: [r"13,[1-4],14,[1-4]"],
         9: [r"11,([1-4]),14,\1"],
         10: [r"12,([1-4]),13,\1"],
         11: [r"9,[1-4],9,[1-4]"],
         12: [r"10,([1-4]),14,\1"],
         13: [r"12,[1-4],14,[1-4]"],
         14: [r"11,([1-4]),13,\1"],
         15: [r"8,[1-4],8,[1-4]"],
         16: [r"11,([1-4]),12,\1"],
         17: [r"10,([1-4]),13,\1"],
         18: [r"9,([1-4]),14,\1", r"11,[1-4],14,[1-4]"],
         19: [r"10,([1-4]),12,\1"],
         20: [r"12,[1-4],13,[1-4]", r"7,[1-4],7,[1-4]"],
         21: [r"10,([1-4]),11,\1"],
         22: [r"8,([1-4]),14,\1"],
         23: [r"9,([1-4]),13,\1"],
         24: [r"10,[1-4],14,[1-4]", r"5,([1-4]),14,\1", r"7,([1-4]),14,\1", r"11,[1-4],13,[1-4]"],
         25: [r"6,[1-4],6,[1-4]"],
         26: [r"9,([1-4]),10,\1", r"4,([1-4]),14,\1", r"9,([1-4]),12,\1"],
         27: [r"9,([1-4]),11,\1"],
         28: [r"11,[1-4],12,[1-4]", r"6,([1-4]),14,\1"],
         29: [r"5,[1-4],5,[1-4]", r"3,([1-4]),14,\1"],
         30: [r"8,([1-4]),13,\1", r"10,[1-4],13,[1-4]"],
         31: [r"8,([1-4]),9,\1", r"8,([1-4]),10,\1", r"7,([1-4]),13,\1", r"2,([1-4]),14,\1"],
         32: [r"7,([1-4]),8,\1", r"10,[1-4],12,[1-4]", r"8,([1-4]),12,\1"],
         33: [r"4,[1-4],4,[1-4]", r"9,[1-4],14,[1-4]", r"8,([1-4]),11,\1", r"6,([1-4]),7,\1", r"10,[1-4],11,[1-4]"],
         34: [r"7,([1-4]),9,\1", r"6,([1-4]),13,\1"],
         35: [r"5,([1-4]),13,\1", r"4,([1-4]),13,\1", r"7,([1-4]),10,\1"],
         36: [r"7,([1-4]),12,\1"],
         37: [r"9,[1-4],13,[1-4]", r"5,([1-4]),6,\1", r"9,[1-4],10,[1-4]", r"6,([1-4]),8,\1", r"8,[1-4],14,[1-4]",
              r"7,([1-4]),11,\1", r"3,[1-4],3,[1-4]"],
         38: [r"4,([1-4]),5,\1", r"6,([1-4]),12,\1", r"3,([1-4]),13,\1", r"9,[1-4],12,[1-4]"],
         39: [r"5,([1-4]),7,\1", r"2,[1-4],2,[1-4]", r"9,[1-4],11,[1-4]", r"4,([1-4]),6,\1", r"5,([1-4]),12,\1",
              r"2,([1-4]),13,\1", r"6,([1-4]),9,\1"],
         40: [r"3,([1-4]),12,\1", r"8,[1-4],11,[1-4]", r"8,[1-4],9,[1-4]", r"8,[1-4],10,[1-4]", r"7,[1-4],9,[1-4]",
              r"7,[1-4],14,[1-4]", r"7,[1-4],10,[1-4]", r"4,([1-4]),12,\1"],
         41: [r"8,[1-4],12,[1-4]", r"5,([1-4]),11,\1", r"6,[1-4],10,[1-4]", r"5,[1-4],7,[1-4]", r"4,([1-4]),11,\1",
              r"4,([1-4]),7,\1", r"8,[1-4],13,[1-4]", r"6,[1-4],8,[1-4]", r"3,([1-4]),5,\1", r"7,[1-4],13,[1-4]",
              r"3,([1-4]),6,\1", r"6,([1-4]),11,\1", r"5,[1-4],8,[1-4]", r"6,([1-4]),10,\1", r"6,[1-4],7,[1-4]"],
         42: [r"6,[1-4],14,[1-4]", r"2,[1-4],10,[1-4]", r"5,([1-4]),9,\1", r"4,[1-4],8,[1-4]", r"2,[1-4],6,[1-4]",
              r"5,([1-4]),10,\1", r"5,[1-4],9,[1-4]", r"5,[1-4],14,[1-4]", r"7,[1-4],12,[1-4]", r"5,[1-4],10,[1-4]",
              r"7,[1-4],8,[1-4]", r"3,[1-4],8,[1-4]", r"5,[1-4],6,[1-4]", r"2,([1-4]),12,\1", r"4,[1-4],9,[1-4]",
              r"4,[1-4],7,[1-4]", r"4,[1-4],5,[1-4]", r"4,[1-4],14,[1-4]", r"4,[1-4],10,[1-4]", r"2,[1-4],8,[1-4]",
              r"4,[1-4],6,[1-4]", r"2,[1-4],4,[1-4]", r"7,[1-4],11,[1-4]", r"3,[1-4],9,[1-4]", r"5,([1-4]),8,\1",
              r"3,[1-4],7,[1-4]", r"3,[1-4],5,[1-4]", r"3,[1-4],10,[1-4]", r"3,[1-4],6,[1-4]", r"6,[1-4],13,[1-4]",
              r"6,[1-4],11,[1-4]", r"6,[1-4],9,[1-4]", r"2,[1-4],9,[1-4]", r"2,[1-4],7,[1-4]", r"2,[1-4],5,[1-4]"],
         43: [r"4,[1-4],12,[1-4]", r"5,[1-4],13,[1-4]", r"5,[1-4],11,[1-4]", r"3,([1-4]),4,\1", r"3,[1-4],12,[1-4]",
              r"3,[1-4],4,[1-4]", r"4,[1-4],13,[1-4]", r"4,[1-4],11,[1-4]", r"4,([1-4]),10,\1", r"6,[1-4],12,[1-4]",
              r"2,[1-4],12,[1-4]", r"3,([1-4]),11,\1", r"3,[1-4],11,[1-4]", r"3,([1-4]),10,\1", r"3,[1-4],14,[1-4]",
              r"5,[1-4],12,[1-4]", r"2,[1-4],11,[1-4]", r"4,([1-4]),8,\1"],
         44: [r"2,([1-4]),8,\1", r"2,([1-4]),4,\1", r"3,([1-4]),9,\1", r"3,([1-4]),7,\1", r"3,[1-4],13,[1-4]",
              r"2,([1-4]),11,\1", r"2,([1-4]),9,\1", r"2,([1-4]),5,\1", r"2,[1-4],13,[1-4]", r"2,([1-4]),10,\1",
              r"2,([1-4]),6,\1", r"2,[1-4],3,[1-4]"],
         45: [r"2,[1-4],14,[1-4]", r"3,([1-4]),8,\1", r"4,([1-4]),9,\1", r"2,([1-4]),7,\1", r"2,([1-4]),3,\1"]
         }

def get_hole_card_level(hand_card0, hand_card1):
    if hand_card0[0] > hand_card1[0]:
        hand_card0, hand_card1 = hand_card1, hand_card0
    string = "%d,%d,%d,%d" % (hand_card0[0], hand_card0[1], hand_card1[0], hand_card1[1])
    for x in level.keys():
        for y in level[x]:
            if re.findall(y, string):
                return x
