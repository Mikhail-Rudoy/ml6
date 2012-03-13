all:

run: main.py matrix.py screen.py
	python main.py

clean:
	rm *.pyc *~

clear:
	rm *.pyc *~

pic.ppm: run

view: pic.ppm
	display pic.ppm
	rm pic.ppm