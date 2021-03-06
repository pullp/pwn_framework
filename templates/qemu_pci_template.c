/*
launch.sh:
#!/bin/bash
./qemu-system-x86_64 \
    -m 1G \
    -device strng \
    -initrd rootfs.cpio \
    -kernel bzImage \
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
	scp -P5555  -i ./key exp ubuntu@127.0.0.1:/home/ubuntu # use scp
    # find . | cpio -H newc -ov -F ../rootfs.cpio # repack rootfs
	rm exp
*/

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

typedef uint64_t Addr;

#define PMIO_BASE ${PMIO_BASE}
char* MMIO_BASE;

void die(char* msg){
    perror(msg);
    exit(-1);
}

// convert virtual address to physical address
#define PAGE_SHIFT  12
#define PAGE_SIZE   (1 << PAGE_SHIFT)
#define PAGE_MASK (PAGE_SIZE - 1)
#define PFN_PRESENT (1ull << 63)
#define PFN_PFN     ((1ull << 55) - 1)
Addr addr_v2p(Addr v_addr){
    size_t offset;
    uint64_t pme;
    Addr p_addr;
    int fd = open("/proc/self/pagemap", O_RDONLY);
    if (fd < 0)
        die("[addr_v2p] open pagemap failed");
    offset = ((uint64_t) v_addr/PAGE_SIZE)*8;
    if (lseek(fd, offset, SEEK_SET) == -1)
        die("[addr_v2p] lseek failed");
    if (read(fd, &pme, 8) != 8)
        die("[addr_v2p] read from pagemap failed");
    close(fd);
    if (!(pme & PFN_PRESENT))
        return (Addr)-1;
    p_addr = (Addr) ((pme & PFN_PFN) << PAGE_SHIFT);
    p_addr |= (v_addr & PAGE_MASK);
    return p_addr;
}

char* init_mmio_1(char *path, uint32_t size){
    char* res;
    int mmio_fd = open(path, O_RDWR | O_SYNC);
    if (mmio_fd == -1)
        die("[init_mmio_1] open mmio file error");
    res = (char*) mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, mmio_fd, 0);
    if (res == MAP_FAILED)
        die("[init_mmio_1] mmap mmio file failed");
    puts("[init_mmio_1] init success");
    return res;
}

char* init_mmio_2(uint64_t phy_start, uint64_t size){
    char* res;
    char *phymem_path = "/dev/mem";
    if (access(phymem_path, R_OK | W_OK) != 0){
        system("mknod -m 660 /dev/mem c 1 1");
        sleep(1);
        if (access(phymem_path, R_OK | W_OK) != 0)
            die("[init_mmio_2] 'mknod -m 660 /dev/mem c 1 1' failed");
    }
    int phymem_fd = open(phymem_path, O_RDWR | O_SYNC);
    if (phymem_fd == -1)
        die("[init_mmio_2] open /dev/mem failed");
    res = (char*) mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, phymem_fd, phy_start);
    if (res == MAP_FAILED)
        die("[init_mmio_2] mmap /dev/mem failed");
    puts("[init_mmio_2] init success");
    return res;
}

void init_pmio(){
    if (iopl(3) != 0)
        die("[init_pmio] io permission requeset failed");
    puts("[init_pmio] init success");
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
    // MMIO_BASE = init_mmio_1(${MMIO_FILE}, 0x1000); // mmap /sys/devicex/xxx/xxx/resourceN to read/write
    // MMIO_BASE = init_mmio_2(0x000a0000, 0x20000); // mmap /dev/mem to read/write
    init_pmio();

    return 0;

}