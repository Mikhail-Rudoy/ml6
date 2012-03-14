all: main.class screen.class

main.class: main.java
	javac main.java

screen.class: screen.java
	javac screen.java

run: main.class screen.class
	java main

clean:
	rm *~ *.class

clear:
	rm *~ *.class

pic.ppm: run

view: pic.ppm
	display pic.ppm
	rm pic.ppm