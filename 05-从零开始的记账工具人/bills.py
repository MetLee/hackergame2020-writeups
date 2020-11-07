import re
import xlrd


def upper2num(s):
    index = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    rst = 0

    _ = re.findall(r'(.)仟', s)
    if _:
        rst += 100000 * index.index(_[0])

    _ = re.findall(r'(.)佰', s)
    if _:
        rst += 10000 * index.index(_[0])

    _ = re.findall(r'(.)拾', s)
    if _:
        rst += 1000 * index.index(_[0])

    if re.match(r'^拾', s):  # 拾几元 √  壹拾几元 ×
        rst += 1000

    _ = re.findall(r'(.)元', s)
    if _:
        if _[0] in index:
            rst += 100 * index.index(_[0])

    _ = re.findall(r'(.)角', s)
    if _:
        rst += 10 * index.index(_[0])

    _ = re.findall(r'(.)分', s)
    if _:
        rst += 1 * index.index(_[0])

    return rst


def main():
    workbook = xlrd.open_workbook('bills.xlsx')
    worksheet1 = workbook.sheet_by_name(u'Sheet1')

    rst = 0

    num_rows = worksheet1.nrows
    for curr_row in range(1, num_rows):
        row = worksheet1.row_values(curr_row)
        money = upper2num(row[0])
        rst += money * int(row[1])

    rst /= 100
    print(f'flag{{{rst}}}')


if __name__ == '__main__':
    main()
