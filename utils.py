#coding:utf-8
import pwn
import os
import sys
import shutil


"""
Force to use assigned new ld.so by changing the binary
"""
def change_ld(binary, version, copy=True):
    def _cp_ld_libc(_version):
        ld_path = "/home/pu1p/glibcs/ld_and_libcs_x64/ld_%s.so"%(_version)
        libc_path = "/home/pu1p/glibcs/ld_and_libcs_x64/libc_%s.so"%(_version)
        print(ld_path)
        print(libc_path)
        if not os.path.exists(ld_path):
            return ""
        os.system("cp %s ./"%(ld_path))
        os.system("cp %s ./"%(libc_path))
        return "ld_%s.so"%(_version)

    if copy:
        ld = _cp_ld_libc(version)
        if ld == "":
            print("version not exist")
            return -1
    else:
        ld = version
    if not os.access(ld, os.R_OK): 
        pwn.log.failure("Invalid path {} to ld".format(ld))
        return None
    if not os.access(binary, os.R_OK): 
        pwn.log.failure("Invalid path {} to binary".format(binary))
        return None
    binary = pwn.ELF(binary)
    path = './{}_{}'.format(os.path.basename(binary.path), ld.split('.')[-2])
    if os.access(path, os.F_OK):
        os.remove(path)
        print("remove exist file.....")
        # return pwn.ELF(path)
    for segment in binary.segments:
        # print(segment.header['p_type'])
        if segment.header['p_type'] == 'PT_INTERP':
            # print("into this")
            size = segment.header['p_memsz']
            addr = segment.header['p_paddr']
            data = segment.data()
            if size <= len(ld):
                pwn.log.failure("Failed to change PT_INTERP from {} to {}".
                format(data, ld))
                return None
            binary.write(addr, ld.ljust(size, '\x00'))
            break
    binary.save(path)    
    os.chmod(path, 0b111000000) #rwx------
    pwn.log.info("PT_INTERP has changed from {} to {}. Using temp file {}".format(data, ld, path)) 
    return pwn.ELF(path)
  
def template(filename, host="", port=0):
    tp = ""
    with open("/mnt/hgfs/codes/pwn/pwn_framework/template.py", "r") as f1:
        tp = f1.read()

    if "/" in filename:
        filename = filename.split("/")[-1]
    tp = tp.replace("ARCH", pwn.ELF(filename).arch)
    tp = tp.replace("FILENAME", filename)
    tp = tp.replace("HOST", host)
    tp = tp.replace("PORT", str(port))

    with open("exp.py", "w") as f2:
        f2.write(tp)

def test():
    shutil.copy("/mnt/hgfs/codes/pwn/pwn_framework/test.c", "./test.c")
    shutil.copy("/mnt/hgfs/codes/pwn/pwn_framework/Makefile", "./Makefile")
