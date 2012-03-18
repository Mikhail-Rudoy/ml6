OBJECTS: Matrix.class EdgeMatrix.class Canvas.class gui.class

all: $(OBJECTS)

Matrix.class: Matrix.java
	javac Matrix.java

EdgeMatrix.class: Matrix.java EdgeMatrix.java
	javac EdgeMatrix.java

Canvas.class: Canvas.java EdgeMatrix.java
	javac Canvas.java

gui.class: gui.java Canvas.java Matrix.java EdgeMatrix.java
	javac gui.java

run: guiBasic.class
	java gui

clean:
	rm *~ *.class

clear:
	rm *~ *.class