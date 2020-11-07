# 自复读的复读机

题面

> 能够复读其他程序输出的程序只是普通的复读机。
>
> 顶尖的复读机还应该能复读出自己的源代码。
>
> 什么是国际复读机啊（战术后仰）
>
> 你现在需要编写两个只有一行 Python 代码的顶尖复读机：
>
> - 其中一个要输出代码本身的逆序（即所有字符从后向前依次输出）
> - 另一个是输出代码本身的 sha256 哈希值，十六进制小写
>
> 满足两个条件分别对应了两个 flag。
>
> 快来开始你的复读吧~



面向百度编程，搜索`输出 自身 逆序`、`输出 自身 hash`都找不到任何结果。

后来某次机缘巧合下搜索`输出 自身`，找到了一篇知乎专栏 https://zhuanlan.zhihu.com/p/34882073 。

于是稍微改改就可以拿来过题了。

### 逆序

```python
quotation = chr(0x22);s = "quotation = chr(0x22);s = {0}{1}{0};s = s.format(quotation, s);print(s[::-1], end='')";s = s.format(quotation, s);print(s[::-1], end='')
```

得到flag1：`flag{Yes!_Y0U_h4v3_a_r3v3rs3d_Qu1ne_62072077e5}`。

### sha256

```python
import hashlib;quotation = chr(0x22);s = "import hashlib;quotation = chr(0x22);s = {0}{1}{0};s = s.format(quotation, s);print(hashlib.sha256(s.encode()).hexdigest(), end='')";s = s.format(quotation, s);print(hashlib.sha256(s.encode()).hexdigest(), end='')
```

得到flag2：`flag{W0W_Y0Ur_c0de_0utputs_1ts_0wn_sha256_4e5955ff91}`。



## 后记

最开始题目理解错误，以为是要输出题目自身的逆序（

尝试了一下：

```python
import os;print(os.system('ls'))
```

输出

```
bin
boot
checker.py
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
runner.py
sbin
srv
sys
tmp
usr
var
0
```

然后尝试

```python
with open('checker.py','r') as f: print(''.join(f.readlines()))
```

得到`checker.py`的源码

```python
import subprocess
import hashlib

if __name__ == "__main__":
    code = input("Your one line python code to exec(): ")
    print()
    if not code:
        print("Code must not be empty")
        exit(-1)
    p = subprocess.run(
        ["su", "nobody", "-s", "/bin/bash", "-c", "/usr/local/bin/python3 /runner.py"],
        input=code.encode(),
        stdout=subprocess.PIPE,
        )
    
    if p.returncode != 0:
        print()
        print("Your code did not run successfully")
        exit(-1)
        
    output = p.stdout.decode()
    
    print("Your code is:")
    print(repr(code))
    print()
    print("Output of your code is:")
    print(repr(output))
    print()
    
    print("Checking reversed(code) == output")
    if code[::-1] == output:
        print(open("/root/flag1").read())
    else:
        print("Failed!")
    print()
    
    print("Checking sha256(code) == output")
    if hashlib.sha256(code.encode()).hexdigest() == output:
        print(open("/root/flag2").read())
    else:
        print("Failed!")
```

于是决定**弯道超车**：

```python
with open('/root/flag1','r') as f: print(''.join(f.readlines()))
```

结果：

`PermissionError: [Errno 13] Permission denied: '/root/flag1'`

惨惨



补一个`runner.py`的源码：

```python
exec(input())
```

