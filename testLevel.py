from hole_cards_level import level
import re
# test hold_cards_level
def test():
    count = 0
    for c1 in range(2, 15):
        for cl1 in range(1, 5):
            for c2 in range(2, 15):
                for cl2 in range(1, 5):
                    count += 1
                    string = "%d,%d,%d,%d" % (c1, cl1, c2, cl2)
                    error = 0
                    find = 0
                    for x in level.keys():
                        print(x)
                        for y in level[x]:
                            if re.match(y, string):
                                find = 1
                                break
                            else:
                                error = 1
                        if error:
                            print("Error, string is:", string)
    print(count)



if __name__ == '__main__':
    test()