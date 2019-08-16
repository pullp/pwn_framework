#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>

int main(){
	char buf[0x10];
	read(0, buf, 10);
	free(0);
	void *p1 = malloc(0x10);
	int a = malloc_usable_size(p1);
	// p1 = "abc"
	int b = malloc_usable_size(p1);
	free(p1);
	int c = malloc_usable_size(p1);
	void *p2 = malloc(0x18);
	return 0;
}
