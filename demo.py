import re

# line = "Cats are smarter than dogs"
#
# matchObj = re.match(r'(.*) are (.*?) .*', line)
#
# if matchObj:
#     print ("matchObj.group() : ", matchObj.group())
#     print("matchObj.group(1) : ", matchObj.group(1))
#     print("matchObj.group(2) : ", matchObj.group(2))
# else:
#     print("No match!!")
#
#
s = '玩家名字：@xx@玩家名字：1'
ret = re.match(r'(.*)玩家名字(.*)',s)
print(ret.group(2))

s = "你的ID：1玩家名字：@xx@每人筹码：$108玩家人数：1玩家名字：@xx@@zz@每人筹码：$108$152玩家人数：2玩家名字：@xx@@zz@@cc@每人筹码：$108$152$122"
# temp = re.findall(r"\@(.*?)\@", s)  # 名字

ret = re.match(r".*玩家名字：(.*)", s)
print(ret)
print(ret[1])
if ret:
    tem = re.findall(r"\@(.*?)\@", ret[1])  # 名字
    print(tem)