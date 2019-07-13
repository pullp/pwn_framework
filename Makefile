CC = gcc
CFALGS = -g 

test: test.c
	$(CC) $(CFALGS) $^ -o test.out
