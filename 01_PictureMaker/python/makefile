all:

run: main.py screen.py
	python main.py

clean:
	rm *pyc *~

pic.ppm: run

view: pic.ppm
	display pic.ppm
	rm pic.ppm