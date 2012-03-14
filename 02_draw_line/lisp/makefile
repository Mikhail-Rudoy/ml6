compile: screen.lisp io.lisp curves.lisp
	clisp -q -c screen.lisp io.lisp curves.lisp

run: main.lisp screen.lisp io.lisp curves.lisp
	clisp main.lisp

clean:
	rm *~ *.lib *.fas

clear:
	rm *~ *.lib *.fas

pic.ppm: run

view: pic.ppm
	display pic.ppm
	rm pic.ppm