OBJECTS= main.o draw.o display.o
CFLAGS= -Wall
CC= gcc

all: $(OBJECTS)
	$(CC) -lm -o main.exe $(OBJECTS)

main.o: main.c display.h draw.h ml6.h
	$(CC) -c  main.c

draw.o: draw.c draw.h display.h ml6.h
	$(CC) $(CFLAGS) -c draw.c

dsiplay.o: display.c display.h ml6.h
	$(CC) $(CFLAGS) -c display.c

run: all
	./main.exe

clean:
	rm *.o *~

clear:
	rm *.o *~ main.exe

view: all
	./main.exe -d