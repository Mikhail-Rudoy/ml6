OBJECTS: Matrix.class EdgeMatrix.class Canvas.class guiBasic.class

all: $(OBJECTS)

Matrix.class: Matrix.java
	javac Matrix.java

EdgeMatrix.class: Matrix.java EdgeMatrix.java
	javac EdgeMatrix.java

Canvas.class: Canvas.java EdgeMatrix.java
	javac Canvas.java

guiBasic.class: guiBasic.java Canvas.java Matrix.java EdgeMatrix.java
	javac guiBasic.java

run: guiBasic.class
	java guiBasic

clean:
	rm *~ *.class