CC = gcc
CFLAGS  = -g -Wall
INCLUDES = -I/home/bo/workspace/libfuse-fuse-3.9.1/include 
LFLAGS = -L/home/bo/workspace/libfuse-fuse-3.9.1/build/lib -lfuse3

default: fifaaFS

# To create the executable file count we need the object files
# countwords.o, counter.o, and scanner.o:
#
fifaaFS:  fiffa.o log.o fault.o 
	$(CC) $(CFLAGS) -o fifaaFS fiffa.o log.o fault.o

# To create the object file countwords.o, we need the source
# files countwords.c, scanner.h, and counter.h:
#
log.o:  log.h params.h log.c
	$(CC) $(CFLAGS) $(INCLUDES) -c log.c

# To create the object file counter.o, we need the source files
# counter.c and counter.h:
#
fault.o:  fault.h params.h
	$(CC) $(CFLAGS) $(INCLUDES) -c fault.c

# To create the object file scanner.o, we need the source files
# scanner.c and scanner.h:
#
fifaa.o:  fifaa.c params.h fault.h log.h
	$(CC) $(CFLAGS) $(INCLUDES) $(LFLAGS) -c fifaa.c

# To start over from scratch, type 'make clean'.  This
# removes the executable file, as well as old .o object
# files and *~ backup files:
#
clean: 
	$(RM) count *.o *~