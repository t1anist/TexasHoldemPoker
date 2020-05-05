import pymysql
from math import ceil


class item:
    def __init__(self, hole_card_level=0, bet_sequence='', stack_commit=0, board_texture=0):
        self.hole_card_level = hole_card_level
        self.bet_sequence = bet_sequence
        self.stack_commit = stack_commit
        self.board_texture = board_texture
        self.action = action_dict.copy()
        self.outcome = outcome_dict.copy()


action_dict = {'f': 0, 'c': 0, 'q': 0, 'h': 0, 'i': 0, 'p': 0, 'd': 0, 'v': 0, 't': 0, 'a': 0}
outcome_dict = {'f': 0, 'c': 0, 'q': 0, 'h': 0, 'i': 0, 'p': 0, 'd': 0, 'v': 0, 't': 0, 'a': 0}
items = []
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='woshi250ma?', db='poker', charset='utf8')
    cursor = db.cursor()
    sql = 'select * from test'
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        find = 0
        for it in items:
            if it.hole_card_level == result[2] and it.bet_sequence == result[3] and it.stack_commit == result[4] and it.board_texture == result[5]:
                find = 1
                it.action[result[6]] += 1
                it.outcome[result[6]] += int(result[7])
                # if it.outcome[result[6]] == 0:
                #     print("Exist")
                #     print(it.action)
                #     print(result)
                break
        if not find:
            temp = item(result[2], result[3], result[4], result[5])
            temp.action[result[6]] += 1
            temp.outcome[result[6]] += int(result[7])
            items.append(temp)
    for it in items:
        outcome_sum = 0
        action_str = ''
        outcome_str = ''
        for key in it.outcome.keys():
            if key is not 'a':
                outcome_str += str(it.outcome[key]) + ','
            else:
                outcome_str += str(it.outcome[key])
            if not it.action[key]:
                continue
            it.outcome[key] = ceil(it.outcome[key] / it.action[key])
            if it.outcome[key] < 0:
                outcome_sum += abs(1 / it.outcome[key])
            else:
                outcome_sum += it.outcome[key]
        if not outcome_sum:
            continue
        for key in it.action.keys():
            if it.outcome[key] < 0:
                it.action[key] = abs(1 / it.outcome[key]) / outcome_sum, 5
            else:
                it.action[key] = it.outcome[key] / outcome_sum, 5
            if key is not 'a':
                action_str += str(it.action[key]) + ','
            else:
                action_str += str(it.action[key])
        sql = 'INSERT INTO result(hole_card_level, bet_sequence, stack_commit, board_texture, action, outcome) \
                VALUES(%d,\'%s\',%d,%d,\'%s\',\'%s\')' % (it.hole_card_level, it.bet_sequence, it.stack_commit,
                                                          it.board_texture, action_str, outcome_str)
        cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()
