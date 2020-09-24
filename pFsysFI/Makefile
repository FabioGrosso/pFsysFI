CC = gcc
CFLAGS  = -g -Wall
INCLUDES = -I/home/bo/workspace/libfuse-fuse-3.9.1/include 
LFLAGS = -L/home/bo/workspace/libfuse-fuse-3.9.1/build/lib -lfuse3

default: fifaaFS


fifaaFS:  fifaa.o log.o fault.o 
	$(CC) $(CFLAGS) $(INCLUDES) $(LFLAGS) -o fifaaFS fifaa.o log.o fault.o

fifaa.o:  fifaa.c params.h fault.h log.h
	$(CC) $(CFLAGS) $(INCLUDES) $(LFLAGS) -c fifaa.c


log.o:  log.h params.h log.c
	$(CC) $(CFLAGS) $(INCLUDES) -c log.c

fault.o:  fault.h params.h
	$(CC) $(CFLAGS) $(INCLUDES) -c fault.c


clean: 
	$(RM) count *.o *~