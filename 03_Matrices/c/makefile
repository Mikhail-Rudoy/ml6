OBJECTS= main.o draw.o display.o matrix.o
CFLAGS= -Wall
CC= gcc

all: $(OBJECTS)
	$(CC) -o main.exe $(OBJECTS)

main.o: main.c display.h draw.h ml6.h matrix.h
	$(CC) -c main.c

draw.o: draw.c draw.h display.h ml6.h matrix.h
	$(CC) $(CFLAGS) -c draw.c

display.o: display.c display.h ml6.h matrix.h
	$(CC) $(CFLAGS) -c display.c

matrix.o: matrix.c matrix.h
	$(CC) $(CFLAGS) -c matrix.c

run: all
	./main.exe

clean:
	rm *.o *~

clear:
	rm *.o *~ main.exe

view: all
	./main.exe -d