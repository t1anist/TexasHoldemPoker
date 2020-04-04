#  103 * 148
# 1360 - 1030 = 330    330/4 = 80
# 148*3=444
play_pos_Dict = {1: [1], 2: [1, 5], 3: [1, 6, 4], 4: [1, 7, 5, 3], 5: [1, 7, 6, 4, 3], 6: [1, 7, 6, 5, 4, 3],
                 7: [2, 8, 7, 6, 5, 4, 3], 8: [1, 8, 7, 6, 5, 4, 3, 2]}
pos_dict = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}
screen_width = 1360  # 屏幕宽度
screen_height = 700  # 屏幕高度
card_width = 103  # 卡片宽度
card_height = 148  # 卡片高度
d_width = (screen_width - card_width * 10) / 4
center_x1 = center_x5 = int(screen_width / 2)  # 1,5相对
center_x2 = center_x4 = int(center_x1 + d_width + card_width * 2)  # 2，4相对
center_x3 = int(center_x2 + d_width + card_width * 2)  # 3在最右边
center_x6 = center_x8 = int(center_x1 - d_width - card_width * 2)  # 6，8相对
center_x7 = int(center_x6 - d_width - card_width * 2)  # 7在最左边
center_y3 = center_y7 = int(screen_height / 2)
bottom_y1 = bottom_y2 = bottom_y8 = screen_height - 30
top_y4 = top_y5 = top_y6 = 30
