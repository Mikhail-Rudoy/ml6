all: example.txt main.py matrix.py screen.py script.py
	python main.py

clean:
	rm *.pyc *~

clear:
	rm *.pyc *~

example: all
	python main.py example.txt
	display pic1.ppm
	display pic2.ppm
	display pic3.ppm
	display pic3big.ppm
	rm pic1.ppm pic2.ppm pic3.ppm pic3big.ppm