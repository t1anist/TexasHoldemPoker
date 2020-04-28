import pymysql


class item:
    def __init__(self, hole_card_level=0, bet_sequence='', stack_commit='', board_texture=0, action=0, outcome=0):
        self.hole_card_level = hole_card_level
        self.bet_sequence = bet_sequence
        self.stack_commit = stack_commit
        self.board_texture = board_texture
        self.action = action
        self.outcome = outcome


action_dict = {'f': 0, 'c': 0, 'q': 0, 'h': 0, 'i': 0, 'p': 0, 'd': 0, 'v': 0, 't': 0, 'a': 0}
outcome = {'f': 0, 'c': 0, 'q': 0, 'h': 0, 'i': 0, 'p': 0, 'd': 0, 'v': 0, 't': 0, 'a': 0}
items = []
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='woshi250ma?', db='poker', charset='utf8')
    cursor = db.cursor()
    sql = 'select * from test'
    results = cursor.fetchall()
    for result in results:
        for it in items:
            if it.hole_card_level == result[2] and it.bet_sequence == result[3] and it.stack_commit == result[4] and it.board_texture == result[5]:
                it.action[result[6]] += 1
                it.outcome[result[6]] += result[7]
            else:
                temp = item(result[2], result[3], result[4], result[5])
                temp.action = action_dict.copy()
                temp.outcome = outcome.copy()
                items.append(temp)
                it.action[result[6]] += 1
                it.outcome[result[6]] += result[7]
    # TODO : finish result

