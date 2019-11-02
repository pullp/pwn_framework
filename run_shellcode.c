#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>

int main(int argc, char **argv){
	if (argc != 2)
		printf("Usage: ./exec_sc sc_file")
	
	int sc_fd = open(argv[0], O_RDONLY);
	// int sc_fd = open("./bin2", O_RDONLY);
	struct stat sb;
	fstat(sc_fd, &sb);
	printf("sc_file' size : %d", (unsigned int)sb.st_size);
	void *mem = mmap(0, sb.st_size, PROT_READ|PROT_WRITE, MAP_PRIVATE, sc_fd, 0);
	// void *mem = mmap(0, sb.st_size, PROT_READ|PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, , 0);
	if (mem == MAP_FAILED){
		printf("mmap failed");
		return -1;
	}
	mprotect(mem, sb.st_size, PROT_READ|PROT_WRITE|PROT_EXEC);
	((void(*)(void))mem)();
	return 0;
}
