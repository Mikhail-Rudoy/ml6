OBJECTS= main.o draw.o display.o matrix.o parser.o
CFLAGS= -Wall
LDFLAGS = -lm
CC= gcc

all: $(OBJECTS)
	$(CC) -o main.exe $(OBJECTS) $(LDFLAGS)

main.o: main.c display.h draw.h ml6.h matrix.h parser.h
	$(CC) -c main.c

draw.o: draw.c draw.h display.h ml6.h matrix.h
	$(CC) $(CFLAGS) -c draw.c

display.o: display.c display.h ml6.h matrix.h
	$(CC) $(CFLAGS) -c display.c

matrix.o: matrix.c matrix.h
	$(CC) $(CFLAGS) -c matrix.c

parser.o: parser.c parser.h matrix.h draw.h display.h ml6.h
	$(CC) $(CFLAGS) -c parser.c

example1: all example1.txt
	./main.exe example1.txt

example2: all example2.txt
	./main.exe example2.txt

clean:
	rm *.o *~

clear:
	rm *.o *~ main.exe