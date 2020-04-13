<!-- TOC -->

- [1. about pwn_framework](#1-about-pwnframework)
- [2. Install](#2-install)
- [3. generate exp template](#3-generate-exp-template)
  - [3.1. some notes about the exp template](#31-some-notes-about-the-exp-template)
    - [3.1.1. some abbreviations](#311-some-abbreviations)
    - [3.1.2. bps](#312-bps)
    - [3.1.3. gds](#313-gds)
    - [3.1.4. mydebug(io)](#314-mydebugio)
- [4. change ld of a elf file](#4-change-ld-of-a-elf-file)
- [5. 一些常见利用方式的模板](#5-%e4%b8%80%e4%ba%9b%e5%b8%b8%e8%a7%81%e5%88%a9%e7%94%a8%e6%96%b9%e5%bc%8f%e7%9a%84%e6%a8%a1%e6%9d%bf)
- [6. 关于环境配置的一些脚本](#6-%e5%85%b3%e4%ba%8e%e7%8e%af%e5%a2%83%e9%85%8d%e7%bd%ae%e7%9a%84%e4%b8%80%e4%ba%9b%e8%84%9a%e6%9c%ac)

<!-- /TOC -->


# 1. about pwn_framework
本项目包含一些为了避免每次做pwn题时候的重复工作的脚本以及一些利用方式的模板

requirements:
- python2
- tmux
- pwntools (a python library)


# 2. Install

首先将本项目clone到本地

```
git clone https://github.com/pullp/pwn_framework
```

然后添加到 python path 中

```bash
export PYTHONPATH=path/to/parent/dir
```

example:

```bash
# the project's path is /mnt/hgfs/codes/pwn/pwn_framework
export PYTHONPATH="/mnt/hgfs/codes/pwn"
```

*可以把命令添加到 bashrc 中*

之后就可以在 python 中import并使用 pwn_framework 了

# 3. generate exp template

```python
import pwn_framework as pf
pf.utls.template("file name", "host", port)
# pf.utls.template("file name", "host:port")
# pf.utls.template("file name", "host port")
```

然后就可以在当前目录下找到生成的`exp.py` 了

Example

```python
import pwn_framework as pf
pf.utils.template("./starbound", "chall.pwnable.tw 10202")
```

## 3.1. some notes about the exp template

### 3.1.1. some abbreviations

对于pwntools中一些常用的交互函数设置了一些缩写

```
io.recvuntil(x)         -> ru(io, x)
io.send(x)              -> sn(io, x)
io.recvline()           -> rl(io)
io.sendline(x)          -> sl(io, x)
io.recv(numb = x)       -> rv(io, x)
io.sendafter(a,b)       -> sa(io, x)
io.sendlineafter(a,b)   -> sla(io, x)
io.recvrepeat(t)        -> rr(io, t)
```

### 3.1.2. bps 
`breakpoints` 的缩写. 是一个`list`. 可以往里面添加地址(类型为`int`), 在用 `mydebug` 启动调试的时候会自动在`list`中的地址上下断点

### 3.1.3. gds
`gdb debug symbols` 的缩写. 一个字典. `key`对应`symbol`的名称,`value`对应`symbol`的地址,在使用`mydebug` 启动调试的时候会自动进行设置,方便调试的时候查看各个地址的内容.

举个例子:

```python
gds['ptrs'] = 0x60020
mydebug(io)
```

然后在gdb窗口中就可以使用如下命令查看 0x60020处的内容

```
> x/10xg $ptrs
...
```

### 3.1.4. mydebug(io)
用来启动gdb.会将原先的窗口窗口竖直切分成两个新的窗口,一边是原先的python脚本界面,另一边是gdb界面(需要 `tmux` ).当gdb退出的时候gdb所在的窗口会被删除,恢复到原先只有一个窗口的状态.

效果图如下:

![mydebug(io) 效果图](.imgs/mydebug.png)

# 4. change ld of a elf file

这个功能需要自己编译各个版本的libc, 具体参考[这篇文章](https://www.jianshu.com/p/ee1ad4044ef7)

*其实直接下载别人编译好的也不是不能用，但是那样调试的时候看不到源码不太方便。并且编译libc也不是很麻烦*

这个功能目前要用的话需要修改`utils.py`中`change_ld()`函数中的路径，指向自己存储各个版本libc 和 ld 的位置

```python
import pwn_framework as pf
pf.utils.change_ld("file name", "version") # such as 2.23
```

# 5. 一些常见利用方式的模板

- off-by-null
- ret2dl_resolve


# 6. 关于环境配置的一些脚本

基于ubuntu 16.04/18.04 配置pwn环境的脚本