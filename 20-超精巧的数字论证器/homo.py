import copy
import json

SOURCE_STR = '114514'
LEN_SOURCE_STR = len(SOURCE_STR)
MAX_PERTURBATION = 9


# 插空
def divide(s):
    if len(s) == 2:
        return [[s], [s[0], s[1]]]
    elif len(s) > 2:
        s_end = s[-1]
        rst = []
        for item in divide(s[:-1]):
            _0 = item.copy()
            _1 = item.copy()
            _0[-1] += s_end
            _1.append(s_end)
            rst.append(_0)
            rst.append(_1)
        return rst
    else:
        return []


# 转int
def str2int(str_list):
    int_list = []
    for str_item in str_list:
        int_item = []
        for s in str_item:
            int_item.append(int(s))
        int_list.append(int_item)
    return int_list


# 运算符
class Operation():
    operators = ['%', '*', '+', '-', '&', '|', '^']
    priority = {
        '~': 10,
        '%': 9,
        '*': 9,
        '+': 8,
        '-': 8,
        '&': 7,
        '|': 6,
        '^': 6
    }
    operate = {
        '~': lambda n: ~n,
        '%': lambda a, b: a % b,
        '*': lambda a, b: a * b,
        '-': lambda a, b: a - b,
        '+': lambda a, b: a + b,
        '&': lambda a, b: a & b,
        '|': lambda a, b: a | b,
        '^': lambda a, b: a ^ b
    }

    def __init__(self):
        pass


# 构建表达式
class Expression():
    def __init__(self, val: int, perturbation: int = 0):
        self.val = val + perturbation
        if val >= 0:
            self.opr = '+'
            self.exp = str(val)
        else:
            self.opr = '-'
            self.exp = '(' + str(val) + ')'
        if perturbation:
            self.exp = '(' + '-~' * perturbation + self.exp + ')'
        self.priority = 10

    def add_node(self, opr: str, rval: int, perturbation: int = 0):
        self.val = Operation.operate[opr](self.val, rval + perturbation)
        if Operation.priority[opr] > self.priority:
            self.exp = '(' + self.exp + ')'
        if perturbation:
            rexp = '(' + '-~' * perturbation + str(rval) + ')'
        else:
            rexp = str(rval)
        self.exp = self.exp + opr + rexp
        self.opr = opr
        self.priority = Operation.priority[opr]

    def get_exp(self):
        return self.exp


# 遍历运算符
class Expressions():
    def __init__(self, val: int):
        self.expressions = {}
        for perturbation in range(0, MAX_PERTURBATION + 1):
            self.expressions[val] = Expression(val, perturbation)
            self.expressions[-val] = Expression(-val, perturbation)

    def add_num(self, rval: int):
        new_expressions = {}
        for lval, expression in self.expressions.items():
            for opr in Operation.operators:
                for perturbation in range(0, MAX_PERTURBATION + 1):
                    _ = copy.copy(expression)
                    _.add_node(opr, rval, perturbation)
                    if _.val not in new_expressions or len(new_expressions[_.val].get_exp()) > len(_.get_exp()):
                        new_expressions[_.val] = _
        self.expressions = new_expressions

    def output(self):
        out = {}
        for val, expression in self.expressions.items():
            if val not in out or len(out[val]) > len(expression.get_exp()):
                out[val] = expression.get_exp()
        return out


def main():
    int_list = str2int(divide(SOURCE_STR))
    int_list.reverse()
    rst = {}
    for pattern in int_list:
        print(pattern)
        exps = Expressions(pattern[0])

        for i in pattern[1:]:
            exps.add_num(i)
        outputs = exps.output()
        del exps

        for val, exp in outputs.items():
            if val not in rst or len(rst[val]) > len(exp):
                rst[val] = exp

    with open('homo.txt', 'w') as f:
        json.dump(rst, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
