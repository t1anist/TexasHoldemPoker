from hole_cards_level import level
import re
# test hold_cards_level
def test():
    count = 0
    success = 0
    for c1 in range(2, 15):
        for cl1 in range(1, 5):
            for c2 in range(c1, 15):
                for cl2 in range(1, 5):
                    if c1 == c2 and cl1 >= cl2:
                        continue
                    count += 1
                    string = "%d,%d,%d,%d" % (c1, cl1, c2, cl2)
                    find = 0
                    reg = ""
                    for x in level.keys():
                        for y in level[x]:
                            if re.findall(y, string):
                                find = x
                                reg = y
                                break
                        if find:
                            break
                    if not find:
                        print("Error: string is ", string)
                    else:
                        print(string, "reg is ", reg, "value is ", find)
                        success += 1
    print("count = ", count, "success = ", success)

# def test1(string):
#     find = 0
#     for x in level.keys():
#         for y in level[x]:
#             if re.findall(y, string):
#                 find = 1
#                 print("reg is ", y, "value is ", x)
#                 break
#         if find:
#             break




if __name__ == '__main__':
    test()
   # test1("14,1,14,2")