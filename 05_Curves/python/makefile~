all: main.py matrix.py screen.py script.py draw.py
	python main.py

clean:
	rm *.pyc *~

clear:
	rm *.pyc *~

example1: all example1.txt
	python main.py example1.txt
	display pic1.ppm
	display pic2.ppm
	display pic3.ppm
	display pic4.ppm
	display pic5.ppm
	rm pic1.ppm pic2.ppm pic3.ppm pic4.ppm pic5.ppm

example2: all example2.txt
	python main.py example2.txt
	display pic1.ppm
	display pic2.ppm
	display pic3.ppm
	display pic3big.ppm
	rm pic1.ppm pic2.ppm pic3.ppm pic3big.ppm