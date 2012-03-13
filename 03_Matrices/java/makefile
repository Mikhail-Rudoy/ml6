OBJECTS: Matrix.class EdgeMatrix.class Frame.class test.class

all: $(OBJECTS)

Matrix.class: Matrix.java
	javac Matrix.java

EdgeMatrix.class: Matrix.java EdgeMatrix.java
	javac EdgeMatrix.java

Frame.class: Frame.java EdgeMatrix.java
	javac Frame.java

test.class: test.java Frame.java Matrix.java EdgeMatrix.java
	javac test.java

run: test.class
	java test

view: test.class
	java test
	display pic.png
	rm pic.png

clean:
	rm *~ *.class

clear:
	rm *~ *.class