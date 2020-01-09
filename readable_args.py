#coding:utf-8
from ast import literal_eval

def _get_args(s):
    if "("  in s:
        s = s[s.find("(")+1:]
    if ")" in s:
        s = s[:s.find(")")]
    return s.split(",")

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
    args = _get_args(s)
    fn = args[0]
    child_stack = args[1]
    flags = args[2]
    rest_args = ", ".join(args[3:])
    #todo

def socket(s):
    # int socket(int domain, int type, int protocol);
    args = _get_args(s)


# finished
def mmap(s):
    def show_prot(prot_int):
        # from glibc-2.23 mman.h
        prots = {"PROT_NONE"	: 0x00,
            "PROT_READ"	: 0x04,
            "PROT_WRITE"	: 0x02,
            "PROT_EXEC"	: 0x01
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
    prot = eval(args[2])
    flags = eval(args[3])
    fd = args[4]
    offset = args[5]
    print("addr is : "+ addr)
    print("length is : "+length)
    show_prot(prot)
    show_flags(flags)
    print("fd is : "+fd)
    print("offset is : "+offset)
    






