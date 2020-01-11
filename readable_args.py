#coding:utf-8
from ast import literal_eval

def _get_args(s):
    if "("  in s:
        s = s[s.find("(")+1:]
    if ")" in s:
        s = s[:s.find(")")]
    res = s.split(",")
    res_strip = []
    for i in res:
        res_strip.append(i.strip())
    return res_strip

def socket(s):
    # int socket(int domain, int type, int protocol);
    args = _get_args(s)


# finished
def signal(sig_int, print2stdout=True):
    sig_map = {'SIGHUP' : 1,
        'SIGINT' : 2,
        'SIGQUIT' : 3,
        'SIGILL' : 4,
        'SIGABRT' : 6,
        'SIGTRAP' : 5,
        # #define	SIGABRT		SIGIOT	/* Abort (ANSI).  */
        'SIGIOT' : 6,
        'SIGEMT' : 7,
        'SIGFPE' : 8,
        'SIGKILL' : 9,
        'SIGBUS' : 10,
        'SIGSEGV' : 11,
        'SIGSYS' : 12,
        'SIGPIPE' : 13,
        'SIGALRM' : 14,
        'SIGTERM' : 15,
        'SIGURG' : 16,
        'SIGSTOP' : 17,
        'SIGTSTP' : 18,
        'SIGCONT' : 19,
        'SIGCHLD' : 20,
        # #define	SIGCLD		SIGCHLD	/* Same as SIGCHLD (System V).  */
        'SIGCLD' : 20,
        'SIGTTIN' : 21,
        'SIGTTOU' : 22,
        'SIGIO' : 23,
        # #define	SIGPOLL		SIGIO	/* Same as SIGIO? (SVID).  */
        'SIGPOLL' : 23,
        'SIGXCPU' : 24,
        'SIGXFSZ' : 25,
        'SIGVTALRM' : 26,
        'SIGPROF' : 27,
        'SIGWINCH' : 28,
        'SIGINFO' : 29,
        'SIGUSR1' : 30,
        'SIGUSR2' : 31,
        'SIGLOST' : 32,}
    res = ""
    for s in sig_map:
        if sig_int == sig_map[s]:
            res += (s + " / ")
            # print("signal %s : %d"%(s, sig_int))
            # return s
    if res == "":
        if print2stdout:
            print("invalid signal")
    else:
        res = res[:-2]
        if print2stdout:
            print("signal %s : %d"%(res, sig_int))
    return res

def iofile_flags(flag):
    if type(flag) == str:
        flag = literal_eval(flag)
    # from glibc 2.23
    defines = {'_IO_USER_BUF' : 1,
        '_IO_UNBUFFERED' : 2,
        '_IO_NO_READS' : 4,
        '_IO_NO_WRITES' : 8,
        '_IO_EOF_SEEN' : 0x10,
        '_IO_ERR_SEEN' : 0x20,
        '_IO_DELETE_DONT_CLOSE' : 0x40,
        '_IO_LINKED' : 0x80,
        '_IO_IN_BACKUP' : 0x100,
        '_IO_LINE_BUF' : 0x200,
        '_IO_TIED_PUT_GET' : 0x400,
        '_IO_CURRENTLY_PUTTING' : 0x800,
        '_IO_IS_APPENDING' : 0x1000,
        '_IO_IS_FILEBUF' : 0x2000,
        '_IO_BAD_SEEN' : 0x4000,
        '_IO_USER_LOCK' : 0x8000,
    }
    flag_res = ""
    for d in defines:
        if (flag & defines[d]) != 0:
            flag_res += (d + " | ")
    flag_res = flag_res[:-2]
    print("iofile._flags is : "+flag_res)

def clone(s):
    def show_flags(flag_int):
        flags = {'CLONE_VM': 0x00000100,
            'CLONE_FS': 0x00000200,
            'CLONE_FILES': 0x00000400,
            'CLONE_SIGHAND': 0x00000800,
            'CLONE_PTRACE': 0x00002000,
            'CLONE_VFORK': 0x00004000,
            'CLONE_PARENT': 0x00008000,
            'CLONE_THREAD': 0x00010000,
            'CLONE_NEWNS': 0x00020000,
            'CLONE_SYSVSEM': 0x00040000,
            'CLONE_SETTLS': 0x00080000,
            'CLONE_PARENT_SETTID': 0x00100000,
            'CLONE_CHILD_CLEARTID': 0x00200000,
            'CLONE_DETACHED': 0x00400000,
            'CLONE_UNTRACED': 0x00800000,
            'CLONE_CHILD_SETTID': 0x01000000,
            'CLONE_NEWUTS':	0x04000000,
            'CLONE_NEWIPC':	0x08000000,
            'CLONE_NEWUSER':	0x10000000,
            'CLONE_NEWPID':	0x20000000,
            'CLONE_NEWNET':	0x40000000,
            'CLONE_IO':	0x80000000,}
        readable_flags = ""
        exit_signal = flag_int & 0xff
        if exit_signal:
            readable_flags += "exit_signal : %s\nflag is : "%(signal(flag_int & 0xff, False))
        else:
            readable_flags += "flag is : "
        flag_int &= ~(0xff)
        # print(hex(flag_int))
        for f in flags:
            if (flag_int & flags[f]) != 0:
                readable_flags += (f + " | ")
        readable_flags = readable_flags[:-2]
        print(readable_flags)
        return readable_flags
    args = _get_args(s)
    fn = args[0]
    child_stack = args[1]
    flags = literal_eval(args[2])
    rest_args = "(" + ", ".join(args[3:]) +")"
    # print("bbb")
    #todo
    print("fn : "+fn)
    print("child_stack : "+child_stack)
    show_flags(flags)
    print("rest_args : "+rest_args)

def mmap(s):
    def show_prot(prot_int):
        # from glibc-2.23 mman.h
        prots = {"PROT_NONE"	: 0x00,
            "PROT_READ"	: 0x01,
            "PROT_WRITE"	: 0x02,
            "PROT_EXEC"	: 0x04
        } 
        prot_res = ""
        for p in prots:
            if (prot_int & prots[p]) != 0:
                prot_res += (p + " | ")
        prot_res = prot_res[:-2]
        print("prot is : "+prot_res)

    def show_flags(flag_int):
        # tested under unbuntu 16.04 
        # MAP_HUGE_2MB, MAP_HUGE_1GB and MAP_UNINITIALIZED are undefined
        # MAP_ANON is the same as MAP_ANONYMOUS
        flags = {
            "MAP_SHARED" : 0x1,
            "MAP_PRIVATE" : 0x2,
            "MAP_32BIT" : 0x40,
            "MAP_ANON" : 0x20,
            "MAP_ANONYMOUS" : 0x20,
            "MAP_DENYWRITE" : 0x800,
            "MAP_EXECUTABLE" : 0x1000,
            "MAP_FILE" : 0x0,
            "MAP_FIXED" : 0x10,
            "MAP_GROWSDOWN" : 0x100,
            "MAP_HUGETLB" : 0x40000,
            "MAP_LOCKED" : 0x2000,
            "MAP_NONBLOCK" : 0x10000,
            "MAP_NORESERVE" : 0x4000,
            "MAP_POPULATE" : 0x8000,
            "MAP_STACK" : 0x20000,
        }
        flag_res = ""
        for f in flags:
            if (flag_int & flags[f]) != 0:
                flag_res += (f + " | ")
        flag_res = flag_res[:-2]
        print("flag is : "+flag_res)

    args = _get_args(s)
    addr = args[0]
    length = args[1]
    prot = literal_eval(args[2])
    flags = literal_eval(args[3])
    fd = args[4]
    offset = args[5]
    print("addr is : "+ addr)
    print("length is : "+length)
    show_prot(prot)
    show_flags(flags)
    print("fd is : "+fd)
    print("offset is : "+offset)
    






