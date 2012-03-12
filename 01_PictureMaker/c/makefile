main.exe: maker.c
	gcc maker.c -o main.exe

run: main.exe
	./main.exe

clean:
	rm main.exe

pic.ppm: run
	

view: pic.ppm
	display pic.ppm
	rm pic.ppm