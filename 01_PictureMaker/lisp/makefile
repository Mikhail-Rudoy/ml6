compile:
	clisp -q -c screen.lisp

run: main.lisp screen.lisp
	clisp main.lisp

clean:
	rm *~ *.lib *.fas pic.ppm

clear:
	rm *~ *.lib *.fas

pic.ppm: run

view: pic.ppm
	display pic.ppm
	rm pic.ppm