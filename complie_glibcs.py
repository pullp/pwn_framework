#! /usr/bin/python
import os
import shutil

global GLIBCS_PATH
GLIBCS_PATH = "/var/glibcs"


def compile(version):
    global GLIBCS_PATH
    os.chdir(GLIBCS_PATH)
    os.system("tar zxvf ./glibc-%s.tar.gz"%(version))
    os.mkdir("glibc-%s_build"%(version))
    os.mkdir("glibc-%s_out"%(version))
    os.chdir("glibc-%s_build"%(version))
    os.system("../glibc-%s/configure '--prefix=%s/glibc-%s_out'"%(version, GLIBCS_PATH, version))
    os.system("make && make install")
    os.chdir("../glibc-%s_out/lib"%(version))
    shutil.copy("./libc-%s.so", "../ld_and_libcs_x64/libc_%s.so"%(version, version))
    shutil.copy("./elf/ld-%s.so", "../ld_and_libcs_x64/ld_%s.so"%(version, version))


if __name__ == "__main__":
    compile("2.27")
    compile("2.29")

# CC="gcc -m32" CXX="g++ -m32" \
# CFLAGS="-g -g3 -ggdb -gdwarf-4 -Og -Wno-error" \
# CXXFLAGS="-g -g3 -ggdb -gdwarf-4 -Og" \
# ../configure --prefix=/var/glibcs/glibc-2.23_out --host=i686-linux-gnu