
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
        

