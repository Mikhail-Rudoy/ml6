all:

run: main.lisp screen.lisp
	clisp main.lisp

clean:
	rm *~

pic.ppm: run

view: pic.ppm
	display pic.ppm
	rm pic.ppm