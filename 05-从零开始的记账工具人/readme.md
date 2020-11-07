# 从零开始的记账工具人

题面

> 如同往常一样，你的 npy 突然丢给你一个购物账单：“我今天买了几个小玩意，你能帮我算一下一共花了多少钱吗？”
>
> 你心想：~~又双叒叕要开始吃土了~~ 这不是很简单吗？电子表格里面一拖动就算出来了
>
> 只不过拿到账单之后你才注意到，似乎是为了剁手时更加的安心，这次的账单上面的金额全使用了中文大写数字
>
> **注意：请将账单总金额保留小数点后两位，放在 `flag{}` 中提交，例如总金额为 123.45 元时，你需要提交 `flag{123.45}`**



面向百度编程，发现好像Excel好像不支持带元分角的大写中文转换。

于是随手查了一个在线工具： https://szjrzzwdxje.51240.com/ ，随后用`xlrd`库读xlsx文件，直接去get `https://szjrzzwdxje.51240.com/{金额}__szjrzzwdxje/`，再用正则匹配结果。

看起来挺棒的。

结果flag不对！！！！！！！！！！！！！！！！！！！！！！！

后来打了一下log，发现一个大问题：这个网站不靠谱！！！！

![1](img/1.png)

好吧自己手写parser。

主要思路是两位两位正则，再组合一下。为了防止float坏事，干脆直接乘100，求和之后再除掉。

```python
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
```

得到flag：`flag{18252.29}`。