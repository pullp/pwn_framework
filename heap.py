#coding:utf-8
"""
just for learing
"""
class Heap(object):
    class Chunk(object):
        def __init__(addr, size, fd, bk):
            self.addr = addr
            self.size = size
            self.fd = fd
            self.bk = bk
    
    def __init__(self, base=0x40000, ):
        self.malloc_hook = None
        self.free_hook = None
        self.base = base
        self.us_bin = []
        self.fast_bins = [[] for i in range(2, 9)]
        self.small_bins = [[]]
        # return super().__init__(*args, **kwargs)
    
    def is_fast(self, size):
        return True if size<=0x80 else False
    def fast_size2idx(self, size):
        # ceiling to 0x10
        idx = ((size + 0xf)/0x10)
        if not is_fast(idx * 0x10):
            log.error("wrong fast size for fast_size2idx() : " + str(size))
            exit(-1)
        return idx-2
    def _chunk_is_mapped(self, chunk):
        pass
    def malloc(self, size):
        # not support arena yet
        # not support mutex lock yet
        if self.malloc_hook != None:
            self.malloc_hook(size)
        victim = self.int_malloc(size)

        assert(victim==0 
                or self.chunk_is_mapped(self.mem2chunk(victim)
            )
        
            
    
    def free(self, ptr):
        pass
    
    def calloc(self, ptr):
        pass
        

