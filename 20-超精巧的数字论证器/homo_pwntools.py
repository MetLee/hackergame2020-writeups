import json
import re
from pwn import *


token = 'tooooooooooooooken'


# 如果查不到就在前面加 -~ 微调
def find(db, number):
    if number in db:
        return '(' + db[number] + ')'
    else:
        return '-~' + find(db, number - 1)


def main():
    with open('homo.txt', 'r') as f:
        database = json.load(f)
        database = {int(val): database[val] for val in database.keys()}

    io = remote('202.38.93.111', 10241)
    io.recvline()
    io.sendline(token)

    while True:
        try:
            _ = io.recvline()
            number = re.findall(
                r'Challenge\s*\(\d*/32\):\s*(\d*)', _.decode())[0]
            number = int(number)
            rst = find(database, number)
            io.sendline(rst)
            print(number, rst)
        except:
            print(_)
            break
    input()


if __name__ == '__main__':
    main()
