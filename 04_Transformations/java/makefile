OBJECTS: Parser.class Matrix.class EdgeMatrix.class Frame.class test.class

all: $(OBJECTS)

Parser.class: Parser.java EdgeMatrix.java Matrix.java Frame.java
	javac Parser.java

Matrix.class: Matrix.java
	javac Matrix.java

EdgeMatrix.class: Matrix.java EdgeMatrix.java
	javac EdgeMatrix.java

Frame.class: Frame.java EdgeMatrix.java
	javac Frame.java

test.class: test.java Frame.java Matrix.java EdgeMatrix.java Parser.java
	javac test.java

example1: test.class
	java test example1.txt
	display pic1.png
	display pic2.png
	display pic3.png
	display pic4.png
	display pic5.png
	rm pic1.png pic2.png pic3.png pic4.png pic5.png

example2: test.class
	java test example2.txt
	display pic1.png
	display pic2.png
	display pic3.png
	display pic3big.png
	rm pic1.png pic2.png pic3.png pic3big.png

clean:
	rm *~ *.class

clear:
	rm *~ *.class