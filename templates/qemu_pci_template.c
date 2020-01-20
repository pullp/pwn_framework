/*
launch.sh:
    #!/bin/bash
    ./qemu-system-x86_64 \
        -m 1G \
        -device strng \
        -hda my-disk.img \
        -hdb my-seed.img \
        -nographic \
        -L pc-bios/ \
        -enable-kvm \
        -device e1000,netdev=net0 \
        -netdev user,id=net0,hostfwd=tcp::5555-:22

generate key pair:
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

add public key:
    cat ./key.pub > ~/.ssh/authorized_keys

use scp to transfer file:
    scp -P5555 exp ubuntu@127.0.0.1:/home/ubuntu # use private key
    scp -P5555  -i ./key exp ubuntu@127.0.0.1:/home/ubuntu # use password

login with ssh:
    ssh ubuntu@127.0.0.1 -p 5555 -i ./key

Makefile template:
exp:
	cc -m32 -O0 -static -o exp exp.c
	scp -P5555  -i ./key exp ubuntu@127.0.0.1:/home/ubuntu
	rm exp*/

#include <assert.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>
#include<sys/io.h>

#define MMIO_FILE ${MMIO_FILE}
#define PMIO_BASE ${PMIO_BASE}
char* MMIO_BASE;

void die(char* msg){
    perror(msg);
    exit(-1);
}

void init_io(){
    int mmio_fd = open(MMIO_FILE, O_RDWR | O_SYNC);
    if (mmio_fd == -1)
        die("open mmio file error");
    MMIO_BASE = mmap(0, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, mmio_fd, 0);
    if (MMIO_BASE == MAP_FAILED)
        die("mmap mmio file failed");
    if (iopl(3) != 0)
        die("io permission requeset failed");
}

uint32_t pmio_read(uint32_t offset){
    return (uint32_t)inl(PMIO_BASE + offset);
}

void pmio_write(uint32_t offset, uint32_t val){
    outl(val, PMIO_BASE + offset);
}

uint32_t mmio_read(uint32_t offset){
    return *(uint32_t *)(MMIO_BASE + offset);
}

void mmio_write(uint32_t offset, uint32_t val){
    *(uint32_t *)(MMIO_BASE + offset) = val;
}

/*
cat /root/flag 
0x20746163
0x6f6f722f
0x6c662f74
0x00006761
*/

int main(int argc, char **argv){
    init_io();
    
    return 0;

}