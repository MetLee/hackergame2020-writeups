import json


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

    while True:
        try:
            number = input('输入：')
            number = int(number)
            print(find(database, number))
        except:
            continue


if __name__ == '__main__':
    main()
