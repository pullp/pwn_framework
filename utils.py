#coding:utf-8
import pwn
import os
import sys
import shutil
import re

import pwn_framework.readable_args


"""
Force to use assigned new ld.so by changing the binary
"""
def change_ld(binary, version, copy=True):
    if os.path.exists("/usr/src/glibc"):
        GLIBCS_PATH = "/usr/src/glibc"
    elif os.path.exists("/home/pu1p/glibcs"):
        GLIBCS_PATH = "/home/pu1p/glibcs"
    elif os.path.exists("/var/glibcs"):
        GLIBCS_PATH = "/var/glibcs"
    else:
        print("unknown glibc path")
        return
    def _cp_ld_libc(_version):
        ld_path = "%s/ld_and_libcs_x64/ld_%s.so"%(GLIBCS_PATH, _version)
        libc_path = "%s/ld_and_libcs_x64/libc_%s.so"%(GLIBCS_PATH, _version)
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
            binary.write(addr, ld.ljust(size, '\x00').encode())
            break
    binary.save(path)    
    os.chmod(path, 0b111000000) #rwx------
    pwn.log.info("PT_INTERP has changed from {} to {}. Using temp file {}".format(data, ld, path)) 
    return pwn.ELF(path)
  
def template(filename, host="", port=0):
    if os.path.exists("./exp.py"):
        if (raw_input("do you want to overwrite exist exp.py ? (yes/no)") != "yes"):
            return
    tp = ""
    with open("/mnt/hgfs/codes/pwn/pwn_framework/pwn_framework/templates/template.py", "r") as f1:
        tp = f1.read()

    if "/" in filename:
        filename = filename.split("/")[-1]
    arch = pwn.ELF(filename).arch
    tp = tp.replace("ARCH", arch)
    tp = tp.replace("FILENAME", filename)
    host = host.strip()
    if ":" in host:
        tmp = host.split(":")
        host = tmp[0].strip()
        port = int(tmp[1])
    if " " in host:
        tmp = host.split(" ")
        for i in tmp:
            if i == "":
                continue
            if "." in i:
                host = tmp[0].strip() 
            else:
                port = int(tmp[1])
    tp = tp.replace("HOST", host)
    tp = tp.replace("PORT", str(port))
    print("arch : %s, filename : %s, host : %s, port : %d"%(arch, filename, host, port))
    with open("exp.py", "w") as f2:
        f2.write(tp)

def qemu_pci(mmio_file="/sys/devices/pci0000:00/0000:00:02.0/resource0", pmio_base=0):
    """
    generate exploit template named 'exp.c' at current path, the template is used 
        for challenges about qemu escape with pci device
    @param mmio_file: the device file used to read/write pci device's MMIO space,
        such as /sys/devices/pci0000:00/0000:00:03.0/resource0
    @param pmio_base: the start address of pci device's PMIO space. you can get
        the address by cat the resource file.
    """
    if os.path.exists("./exp.c"):
        if (raw_input("do you want to overwrite exist exp.py ? (yes/no)") != "yes"):
            return
    tp = ""
    tp = open("/mnt/hgfs/codes/pwn/pwn_framework/pwn_framework/templates/qemu_pci_template.c", "r").read()
    tp = tp.replace("${MMIO_FILE}", mmio_file)
    tp = tp.replace("${PMIO_BASE}", hex(pmio_base))
    open("./exp.c", "w").write(tp)

def test():
    shutil.copy("/mnt/hgfs/codes/pwn/pwn_framework/pwn_framework/templates/test.c", "./test.c")
    shutil.copy("/mnt/hgfs/codes/pwn/pwn_framework/pwn_framework/templates/Makefile", "./Makefile")

def publish(exp="./exp.py", out="./public_exp.py"):
    lines = open(exp, "r").readlines()
    lines.reverse()
    s1 = ""
    while True:
        try:
            line = lines.pop()
            if "pf" in line:
                continue
            if "lambda p" in line:
                continue
            # if "context" in line:
            #     continue
            # if "global io" in line:
            #     continue
            # if "LOCAL = 1" in line:
            #     continue
            if "break_points" in line:
                continue
            if "bps" in line:
                continue
            if "gds" in line:
                continue
            if "def _get_bstr(" in line:
                while lines.pop().startswith("  "):
                    continue
                s1 += "\n"
                continue
            if "def wait(" in line:
                while lines.pop().startswith("  "):
                    continue
                s1 += "\n"
                continue
            if "def mydebug(" in line:
                while lines.pop().startswith("  "):
                    continue
                s1 += "\n"
                continue
            if "def pause(" in line:
                while lines.pop().startswith("  "):
                    continue
                s1 += "\n"
                continue
            if "def sh(" in line:
                while lines.pop().startswith("  "):
                    continue
                s1 += "\n"
                continue
            if "wait(" in line:
                second = re.findall(r"\d+\.?\d*", line)[0]
                s1 += line[:line.find("wait(")]+"time.sleep(%s)\n"%(second)
                continue
            if "_get_bstr(" in line or  "pause(" in line \
                or "mydebug(" in line :
                continue

            # if "if LOCAL:" in line:
            #     s1 += "# local\n"
            #     while True:
            #         line = lines.pop()
            #         if line.strip() == "":
            #             continue
            #         if line.startswith("  "):
            #             s1 += "# "+line.strip()+"\n"
            #         elif line.startswith("else:"):
            #             s1 += "# remote\n"
            #         else:
            #             # s1 += "\n"+line
            #             print("append line:"+line)
            #             lines.append(line)
            #             break
            #     continue
            if line.strip(" ").startswith("#"):
                continue
            s1 += line
        except IndexError as e:
            break
    s2 = s1.replace("ru(", "io.recvuntil(")\
            .replace("rv(", "io.recv(")\
            .replace("rl(", "io.recvline(")\
            .replace("sn(", "io.send(")\
            .replace("sa(", "io.sendafter(")\
            .replace("sla(", "io.sendlineafter(")\
            .replace("sl(", "io.sendline(")\
            .replace("(p,", "(")\
            .replace("(io,", "(")
    open(out, "w").write(s2)

def disable_aslr():
    """
    refer to https://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization
    """
    print("echo 0 | sudo tee /proc/sys/kernel/randomize_va_space")
