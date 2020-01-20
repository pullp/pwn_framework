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